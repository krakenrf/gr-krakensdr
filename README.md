This is a GNU Radio Block for KrakenSDR. It connects via a TCP socket connection to the KrakenSDR DAQ server software called Heimdall. Heimdall handles all sample and phase coherence calibration via the noise source, and this block receives the coherent IQ sample output and makes it available for further DSP processing in GNU Radio.

You must set the CPI size setting in the block to be the same as in your Heimdall Firmware/daq_chain_config.ini file.

The block will output a vector that is CPI size number of samples.

# GNU Radio OOT Block Install Instructions

```
sudo apt-get install gnuradio-dev cmake libspdlog-dev clang-format

git clone https://github.com/krakenrf/gr-krakensdr

cd gr-krakensdr
mkdir build
cd build
cmake ..
make
sudo make install
```

# Usage Instructions

Copy the heimdall_only_start.sh file into your krakensdr root directory.

In the heimdall_daq_fw folder edit your Firmware/daq_chain_config.ini file and change out_data_iface_type to eth.

```
[data_interface]
out_data_iface_type = eth
```

Then in the krakensdr root directory run ./heimdall_only_start.sh

Now you can start your GRC file with the KrakenSDR source, and it will make a socket connection to the heimdall code at IP 127.0.0.1. Alternatively, you can run the heimdall code on a networked device, but you will need a fast possibly direct network connection to ensure the network throughput is sufficient to handle the five channels.

## Correlation Check
Also included is a correlator block and example GRC file that can be used to check for sample and phase coherence. To do this you'll need to slightly modify the heimdall core code to make the noise source stay on constantly. Edit the Firmware/_daq_core/rtl_daq.c file with a text editor, and near the end of the file change the last zero in rtlsdr_set_bias_tee_gpio to a '1'. Then in the Firmware/_daq_core folder run 'make'. Be sure to rever this edit and run make again when you're done.

```
else if (noise_source_state == 0){
    //rtlsdr_set_bias_tee_gpio(rtl_rec->dev, 0, 0);
    rtlsdr_set_bias_tee_gpio(rtl_rec->dev, 0, 1);
```    
