#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 KrakenRF Inc.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
import socket
import _thread
from threading import Lock
from gnuradio import gr

from struct import pack,unpack
import sys

class krakensdr_source(gr.sync_block):
    """
    docstring for block krakensdr_source
    """
    def __init__(self, ipAddr="127.0.0.1",port=5000, ctrlPort = 5001, cpi_size=2**20,numChannels=5,freq=416.588,gain=[10.0], debug=False):
        gr.sync_block.__init__(self,
            name="KrakenSDR Source",
            in_sig=None,
            out_sig=[np.complex64] * numChannels)

        self.set_min_output_buffer(cpi_size)
        self.valid_gains = [0, 0.9, 1.4, 2.7, 3.7, 7.7, 8.7, 12.5, 14.4, 15.7, 16.6, 19.7, 20.7, 22.9, 25.4, 28.0, 29.7, 32.8, 33.8, 36.4, 37.2, 38.6, 40.2, 42.1, 43.4, 43.9, 44.5, 48.0, 49.6]

        self.cpi_size = cpi_size
        self.ipAddr = ipAddr
        self.port = port
        self.ctrlPort = ctrlPort
        self.numChannels = numChannels
        self.freq = int(freq*10**6)
        self.gain = gain
        self.debug = debug
        self.iq_header = IQHeader()

        # Data Interface
        self.socket_inst = socket.socket()
        self.receiver_connection_status = False
        self.receiverBufferSize = 2 ** 18

        # Control interface
        self.ctr_iface_socket = socket.socket()
        self.ctr_iface_port = self.ctrlPort
        self.ctr_iface_thread_lock = Lock() # Used to synchronize the operation of the ctr_iface thread

        self.iq_samples = None


    def work(self, input_items, output_items):
        self.get_iq_online()

        #print("iq samples size: " + str(np.shape(self.iq_samples)))

        try:
            #for n in range(self.numChannels):
            #    for i in range(len(self.iq_samples[0,:])):
            #        output_items[n][i] = self.iq_samples[n,i]
            if self.iq_header.frame_type == self.iq_header.FRAME_TYPE_DATA:
                for n in range(self.numChannels):
                    output_items[n][:] = self.iq_samples[n,:]
        except:
            pass

        if self.debug:
            self.iq_header.dump_header()

        return len(output_items[0])

    def stop(self):
        self.eth_close()
        return True

    def set_gain(self, gain):
        self.gain = gain
        self.set_if_gain(self.gain)

    def set_freq(self, freq):
        self.freq = freq
        self.set_center_freq(int(freq*10**6))

    def eth_connect(self):
        """
            Compatible only with DAQ firmwares that has the IQ streaming mode.
            HeIMDALL DAQ Firmware version: 1.0 or later
        """
        try:
            if not self.receiver_connection_status:
                # Establlish IQ data interface connection
                self.socket_inst.connect((self.ipAddr, self.port))
                self.socket_inst.sendall(str.encode('streaming'))
                test_iq = self.receive_iq_frame()

                # Establish control interface connection
                self.ctr_iface_socket.connect((self.ipAddr, self.ctr_iface_port))
                self.receiver_connection_status = True
                self.ctr_iface_init()

                self.set_center_freq(self.freq)
                self.set_if_gain(self.gain)
        except:
            errorMsg = sys.exc_info()[0]
            self.receiver_connection_status = False
            print("Ethernet Connection Failed, Error: " + str(errorMsg))
        return -1


    def ctr_iface_init(self):
        """
            Initialize connection with the DAQ FW through the control interface
        """
        if self.receiver_connection_status: # Check connection
            # Assembling message
            cmd="INIT"
            msg_bytes=(cmd.encode()+bytearray(124))
            try:
                _thread.start_new_thread(self.ctr_iface_communication, (msg_bytes,))
            except:
                errorMsg = sys.exc_info()[0]
                print("Unable to start communication thread")
                print("Error message: {:s}".format(errorMsg))


    def ctr_iface_communication(self, msg_bytes):
        """
            Handles communication on the control interface with the DAQ FW

            Parameters:
            -----------

                :param: msg: Message bytes, that will be sent ont the control interface
                :type:  msg: Byte array
        """
        self.ctr_iface_thread_lock.acquire()
        print("Sending control message")
        self.ctr_iface_socket.send(msg_bytes)

        # Waiting for the command to take effect
        reply_msg_bytes = self.ctr_iface_socket.recv(128)

        print("Control interface communication finished")
        self.ctr_iface_thread_lock.release()

        status = reply_msg_bytes[0:4].decode()
        if status == "FNSD":
            print("Reconfiguration succesfully finished")

        else:
            print("Failed to set the requested parameter, reply: {0}".format(status))

    def set_center_freq(self, center_freq):
        """
            Configures the RF center frequency of the receiver through the control interface

            Paramters:
            ----------
                :param: center_freq: Required center frequency to set [Hz]
                :type:  center_freq: float
        """
        if self.receiver_connection_status: # Check connection
            self.freq = int(center_freq)
            # Set center frequency
            cmd="FREQ"
            freq_bytes=pack("Q",int(center_freq))
            msg_bytes=(cmd.encode()+freq_bytes+bytearray(116))
            try:
                _thread.start_new_thread(self.ctr_iface_communication, (msg_bytes,))
            except:
                errorMsg = sys.exc_info()[0]
                print("Unable to start communication thread")
                print("Error message: {:s}".format(errorMsg))

    def set_if_gain(self, gain):
        """
            Configures the IF gain of the receiver through the control interface

            Paramters:
            ----------
                :param: gain: IF gain value [dB]
                :type:  gain: int
        """
        if self.receiver_connection_status: # Check connection
            cmd="GAIN"

            # Find the closest valid gain to the input gain value
            for i in range(len(gain)):
                gain[i] = min(self.valid_gains, key=lambda x:abs(x-gain[i]))

            gain_list= [int(i * 10) for i in gain]

            print("THE GAINS: " + str(gain_list))

            gain_bytes=pack("I"*self.numChannels, *gain_list)
            msg_bytes=(cmd.encode()+gain_bytes+bytearray(128-(self.numChannels+1)*4))
            try:
                _thread.start_new_thread(self.ctr_iface_communication, (msg_bytes,))
            except:
                errorMsg = sys.exc_info()[0]
                print("Unable to start communication thread")
                print("Error message: {:s}".format(errorMsg))


    def get_iq_online(self):
        """
            This function obtains a new IQ data frame through the Ethernet IQ data or the shared memory interface
        """

        # Check connection
        if not self.receiver_connection_status:
            fail = self.eth_connect()
            if fail:
                return -1

        self.socket_inst.sendall(str.encode("IQDownload")) # Send iq request command
        self.iq_samples = self.receive_iq_frame()

    def receive_iq_frame(self):
        """
            Called by the get_iq_online function. Receives IQ samples over the establed Ethernet connection
        """
        total_received_bytes = 0
        recv_bytes_count = 0
        iq_header_bytes = bytearray(self.iq_header.header_size)  # allocate array
        view = memoryview(iq_header_bytes)  # Get buffer

        while total_received_bytes < self.iq_header.header_size:
            # Receive into buffer
            recv_bytes_count = self.socket_inst.recv_into(view, self.iq_header.header_size-total_received_bytes)
            view = view[recv_bytes_count:]  # reset memory region
            total_received_bytes += recv_bytes_count

        self.iq_header.decode_header(iq_header_bytes)
        # Uncomment to check the content of the IQ header
        #self.iq_header.dump_header()

        incoming_payload_size = self.iq_header.cpi_length*self.iq_header.active_ant_chs*2*int(self.iq_header.sample_bit_depth/8)
        if incoming_payload_size > 0:
            # Calculate total bytes to receive from the iq header data
            total_bytes_to_receive = incoming_payload_size
            receiver_buffer_size = 2**18

            total_received_bytes = 0
            recv_bytes_count = 0
            iq_data_bytes = bytearray(total_bytes_to_receive + receiver_buffer_size)  # allocate array
            view = memoryview(iq_data_bytes)  # Get buffer

            while total_received_bytes < total_bytes_to_receive:
                # Receive into buffer
                recv_bytes_count = self.socket_inst.recv_into(view, receiver_buffer_size)
                view = view[recv_bytes_count:]  # reset memory region
                total_received_bytes += recv_bytes_count

            # Convert raw bytes to Complex float64 IQ samples
            self.iq_samples = np.frombuffer(iq_data_bytes[0:total_bytes_to_receive], dtype=np.complex64).reshape(self.iq_header.active_ant_chs, self.iq_header.cpi_length)

            self.iq_frame_bytes =  bytearray()+iq_header_bytes+iq_data_bytes
            return self.iq_samples
        else:
             return 0

    def eth_close(self):
        """
            Close Ethernet conenctions including the IQ data and the control interfaces
        """
        try:
            if self.receiver_connection_status:
                self.socket_inst.sendall(str.encode('q')) # Send exit message
                self.socket_inst.close()
                self.socket_inst = socket.socket() # Re-instantiating socket

                # Close control interface connection
                exit_message_bytes=("EXIT".encode()+bytearray(124))
                self.ctr_iface_socket.send(exit_message_bytes)
                self.ctr_iface_socket.close()
                self.ctr_iface_socket = socket.socket()

            self.receiver_connection_status = False
        except:
            errorMsg = sys.exc_info()[0]
            print("Error message: {0}".format(errorMsg))
            return -1

        return 0



"""
    Desctiption: IQ Frame header definition
    For header field description check the corresponding documentation
    Total length: 1024 byte
    Project: HeIMDALL RTL
    Author: Tamás Pető
    Status: Finished
    Version history:
            1 : Initial version (2019 04 23)
            2 : Fixed 1024 byte length (2019 07 25)
            3 : Noise source state (2019 10 01)
            4 : IQ sync flag (2019 10 21)
            5 : Sync state (2019 11 10)
            6 : Unix Epoch timestamp (2019 12 17) 
            6a: Frame type defines (2020 03 19)
            7 : Sync word (2020 05 03)
"""
class IQHeader():

    FRAME_TYPE_DATA  = 0
    FRAME_TYPE_DUMMY = 1
    FRAME_TYPE_RAMP  = 2
    FRAME_TYPE_CAL   = 3
    FRAME_TYPE_TRIGW = 4

    SYNC_WORD = 0x2bf7b95a

    def __init__(self):

        #self.logger = logging.getLogger(__name__)
        self.header_size = 1024 # size in bytes
        self.reserved_bytes = 192

        self.sync_word=self.SYNC_WORD        # uint32_t
        self.frame_type=0                    # uint32_t
        self.hardware_id=""                  # char [16]
        self.unit_id=0                       # uint32_t
        self.active_ant_chs=0                # uint32_t
        self.ioo_type=0                      # uint32_t
        self.rf_center_freq=0                # uint64_t
        self.adc_sampling_freq=0             # uint64_t
        self.sampling_freq=0                 # uint64_t
        self.cpi_length=0                    # uint32_t
        self.time_stamp=0                    # uint64_t
        self.daq_block_index=0               # uint32_t
        self.cpi_index=0                     # uint32_t
        self.ext_integration_cntr=0          # uint64_t
        self.data_type=0                     # uint32_t
        self.sample_bit_depth=0              # uint32_t
        self.adc_overdrive_flags=0           # uint32_t
        self.if_gains=[0]*32                 # uint32_t x 32
        self.delay_sync_flag=0               # uint32_t
        self.iq_sync_flag=0                  # uint32_t
        self.sync_state=0                    # uint32_t
        self.noise_source_state=0            # uint32_t
        self.reserved=[0]*self.reserved_bytes # uint32_t x reserverd_bytes
        self.header_version=0                # uint32_t

    def decode_header(self, iq_header_byte_array):
        """
            Unpack,decode and store the content of the iq header
        """
        iq_header_list = unpack("II16sIIIQQQIQIIQIII"+"I"*32+"IIII"+"I"*self.reserved_bytes+"I", iq_header_byte_array)

        self.sync_word            = iq_header_list[0]
        self.frame_type           = iq_header_list[1]
        self.hardware_id          = iq_header_list[2].decode()
        self.unit_id              = iq_header_list[3]
        self.active_ant_chs       = iq_header_list[4]
        self.ioo_type             = iq_header_list[5]
        self.rf_center_freq       = iq_header_list[6]
        self.adc_sampling_freq    = iq_header_list[7]
        self.sampling_freq        = iq_header_list[8]
        self.cpi_length           = iq_header_list[9]
        self.time_stamp           = iq_header_list[10]
        self.daq_block_index      = iq_header_list[11]
        self.cpi_index            = iq_header_list[12]
        self.ext_integration_cntr = iq_header_list[13]
        self.data_type            = iq_header_list[14]
        self.sample_bit_depth     = iq_header_list[15]
        self.adc_overdrive_flags  = iq_header_list[16]
        self.if_gains             = iq_header_list[17:49]
        self.delay_sync_flag      = iq_header_list[49]
        self.iq_sync_flag         = iq_header_list[50]
        self.sync_state           = iq_header_list[51]
        self.noise_source_state   = iq_header_list[52]
        self.header_version       = iq_header_list[52+self.reserved_bytes+1]

    def encode_header(self):
        """
            Pack the iq header information into a byte array
        """
        iq_header_byte_array=pack("II", self.sync_word, self.frame_type)
        iq_header_byte_array+=self.hardware_id.encode()+bytearray(16-len(self.hardware_id.encode()))
        iq_header_byte_array+=pack("IIIQQQIQIIQIII",
                                self.unit_id, self.active_ant_chs, self.ioo_type, self.rf_center_freq, self.adc_sampling_freq,
                                self.sampling_freq, self.cpi_length, self.time_stamp, self.daq_block_index, self.cpi_index,
                                self.ext_integration_cntr, self.data_type, self.sample_bit_depth, self.adc_overdrive_flags)
        for m in range(32):
            iq_header_byte_array+=pack("I", self.if_gains[m])

        iq_header_byte_array+=pack("I", self.delay_sync_flag)
        iq_header_byte_array+=pack("I", self.iq_sync_flag)
        iq_header_byte_array+=pack("I", self.sync_state)
        iq_header_byte_array+=pack("I", self.noise_source_state)

        for m in range(self.reserved_bytes):
            iq_header_byte_array+=pack("I",0)

        iq_header_byte_array+=pack("I", self.header_version)
        return iq_header_byte_array

    def dump_header(self):
        """
            Prints out the content of the header in human readable format
        """
        print("Sync word: {:d}".format(self.sync_word))
        print("Header version: {:d}".format(self.header_version))
        print("Frame type: {:d}".format(self.frame_type))
        print("Hardware ID: {:16}".format(self.hardware_id))
        print("Unit ID: {:d}".format(self.unit_id))
        print("Active antenna channels: {:d}".format(self.active_ant_chs))
        print("Illuminator type: {:d}".format(self.ioo_type))
        print("RF center frequency: {:.2f} MHz".format(self.rf_center_freq/10**6))
        print("ADC sampling frequency: {:.2f} MHz".format(self.adc_sampling_freq/10**6))
        print("IQ sampling frequency {:.2f} MHz".format(self.sampling_freq/10**6))
        print("CPI length: {:d}".format(self.cpi_length))
        print("Unix Epoch timestamp: {:d}".format(self.time_stamp))
        print("DAQ block index: {:d}".format(self.daq_block_index))
        print("CPI index: {:d}".format(self.cpi_index))
        print("Extended integration counter {:d}".format(self.ext_integration_cntr))
        print("Data type: {:d}".format(self.data_type))
        print("Sample bit depth: {:d}".format(self.sample_bit_depth))
        print("ADC overdrive flags: {:d}".format(self.adc_overdrive_flags))
        for m in range(32):
            print("Ch: {:d} IF gain: {:.1f} dB".format(m, self.if_gains[m]/10))
        print("Delay sync  flag: {:d}".format(self.delay_sync_flag))
        print("IQ sync  flag: {:d}".format(self.iq_sync_flag))
        print("Sync state: {:d}".format(self.sync_state))
        print("Noise source state: {:d}".format(self.noise_source_state))

    def check_sync_word(self):
        """
            Check the sync word of the header
        """
        if self.sync_word != self.SYNC_WORD:
            return -1
        else:
            return 0
