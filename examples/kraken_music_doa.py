#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.3.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
import sip
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import krakensdr



from gnuradio import qtgui

class kraken_music_doa(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "kraken_music_doa")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.decimation = decimation = 128
        self.cpi_size = cpi_size = 2**20

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            360,
            0,
            1.0,
            "x-Axis",
            "y-Axis",
            "",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis((-140), 10)
        self.qtgui_vector_sink_f_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0.enable_grid(False)
        self.qtgui_vector_sink_f_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_win)
        self.krakensdr_krakensdr_source_0 = krakensdr.krakensdr_source('127.0.0.1', 5000, 5001, cpi_size, 5, 416.588, [40.2, 40.2, 40.2, 40.2, 40.2], False)
        self.krakensdr_doa_music_0 = krakensdr.doa_music((cpi_size//decimation), 0.34, 5, 'UCA')
        self.fir_filter_xxx_0_0_2 = filter.fir_filter_ccc(decimation, [decimation*2])
        self.fir_filter_xxx_0_0_2.declare_sample_delay(0)
        self.fir_filter_xxx_0_0_1 = filter.fir_filter_ccc(decimation, [decimation*2])
        self.fir_filter_xxx_0_0_1.declare_sample_delay(0)
        self.fir_filter_xxx_0_0_0 = filter.fir_filter_ccc(decimation, [decimation*2])
        self.fir_filter_xxx_0_0_0.declare_sample_delay(0)
        self.fir_filter_xxx_0_0 = filter.fir_filter_ccc(decimation, [decimation*2])
        self.fir_filter_xxx_0_0.declare_sample_delay(0)
        self.fir_filter_xxx_0 = filter.fir_filter_ccc(decimation, [decimation*2])
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.blocks_vector_to_stream_0_3 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, cpi_size)
        self.blocks_vector_to_stream_0_2 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, cpi_size)
        self.blocks_vector_to_stream_0_1 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, cpi_size)
        self.blocks_vector_to_stream_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, cpi_size)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, cpi_size)
        self.blocks_stream_to_vector_0_0_2 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, (cpi_size//decimation))
        self.blocks_stream_to_vector_0_0_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, (cpi_size//decimation))
        self.blocks_stream_to_vector_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, (cpi_size//decimation))
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, (cpi_size//decimation))
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, (cpi_size//decimation))


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_stream_to_vector_0, 0), (self.krakensdr_doa_music_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.krakensdr_doa_music_0, 1))
        self.connect((self.blocks_stream_to_vector_0_0_0, 0), (self.krakensdr_doa_music_0, 2))
        self.connect((self.blocks_stream_to_vector_0_0_1, 0), (self.krakensdr_doa_music_0, 3))
        self.connect((self.blocks_stream_to_vector_0_0_2, 0), (self.krakensdr_doa_music_0, 4))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.fir_filter_xxx_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_1, 0), (self.fir_filter_xxx_0_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_2, 0), (self.fir_filter_xxx_0_0_1, 0))
        self.connect((self.blocks_vector_to_stream_0_3, 0), (self.fir_filter_xxx_0_0_2, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.fir_filter_xxx_0_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.fir_filter_xxx_0_0_0, 0), (self.blocks_stream_to_vector_0_0_0, 0))
        self.connect((self.fir_filter_xxx_0_0_1, 0), (self.blocks_stream_to_vector_0_0_1, 0))
        self.connect((self.fir_filter_xxx_0_0_2, 0), (self.blocks_stream_to_vector_0_0_2, 0))
        self.connect((self.krakensdr_doa_music_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.krakensdr_krakensdr_source_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.krakensdr_krakensdr_source_0, 1), (self.blocks_vector_to_stream_0_0, 0))
        self.connect((self.krakensdr_krakensdr_source_0, 2), (self.blocks_vector_to_stream_0_1, 0))
        self.connect((self.krakensdr_krakensdr_source_0, 3), (self.blocks_vector_to_stream_0_2, 0))
        self.connect((self.krakensdr_krakensdr_source_0, 4), (self.blocks_vector_to_stream_0_3, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "kraken_music_doa")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.fir_filter_xxx_0.set_taps([self.decimation*2])
        self.fir_filter_xxx_0_0.set_taps([self.decimation*2])
        self.fir_filter_xxx_0_0_0.set_taps([self.decimation*2])
        self.fir_filter_xxx_0_0_1.set_taps([self.decimation*2])
        self.fir_filter_xxx_0_0_2.set_taps([self.decimation*2])

    def get_cpi_size(self):
        return self.cpi_size

    def set_cpi_size(self, cpi_size):
        self.cpi_size = cpi_size




def main(top_block_cls=kraken_music_doa, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
