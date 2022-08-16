#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: KrakenSDR Correlator Test
# Description: You must modify the code to have the noise source forced ON in the heimdall code to run this test. Consult krakensdr_docs Wiki for instructions.
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
from gnuradio import eng_notation
from gnuradio import qtgui
import sip
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import krakensdr



from gnuradio import qtgui

class kraken_corr_test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "KrakenSDR Correlator Test", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("KrakenSDR Correlator Test")
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

        self.settings = Qt.QSettings("GNU Radio", "kraken_corr_test")

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
        self.vec_len = vec_len = 2**20
        self.freq = freq = 416.588
        self.fft_cut = fft_cut = 4096

        ##################################################
        # Blocks
        ##################################################
        self._freq_tool_bar = Qt.QToolBar(self)
        self._freq_tool_bar.addWidget(Qt.QLabel("'freq'" + ": "))
        self._freq_line_edit = Qt.QLineEdit(str(self.freq))
        self._freq_tool_bar.addWidget(self._freq_line_edit)
        self._freq_line_edit.returnPressed.connect(
            lambda: self.set_freq(eng_notation.str_to_num(str(self._freq_line_edit.text()))))
        self.top_layout.addWidget(self._freq_tool_bar)
        self.qtgui_vector_sink_f_0_0_0_0 = qtgui.vector_sink_f(
            fft_cut,
            0,
            1.0,
            "x-Axis",
            "y-Axis",
            'X_Corr_04',
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0_0_0.set_y_axis((-50), 0)
        self.qtgui_vector_sink_f_0_0_0_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0_0_0.enable_grid(False)
        self.qtgui_vector_sink_f_0_0_0_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_0_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0_0_0.set_ref_level(0)


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
                self.qtgui_vector_sink_f_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_0_0_0_win)
        self.qtgui_vector_sink_f_0_0_0 = qtgui.vector_sink_f(
            fft_cut,
            0,
            1.0,
            "x-Axis",
            "y-Axis",
            'X_Corr_03',
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0_0.set_y_axis((-50), 0)
        self.qtgui_vector_sink_f_0_0_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0_0.enable_grid(False)
        self.qtgui_vector_sink_f_0_0_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0_0.set_ref_level(0)


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
                self.qtgui_vector_sink_f_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_0_0_win)
        self.qtgui_vector_sink_f_0_0 = qtgui.vector_sink_f(
            fft_cut,
            0,
            1.0,
            "x-Axis",
            "y-Axis",
            'X_Corr_02',
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0.set_y_axis((-50), 0)
        self.qtgui_vector_sink_f_0_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0.enable_grid(False)
        self.qtgui_vector_sink_f_0_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_ref_level(0)


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
                self.qtgui_vector_sink_f_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_vector_sink_f_0_0_win)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            fft_cut,
            0,
            1.0,
            "x-Axis",
            "y-Axis",
            'XCorr_01',
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis((-50), 0)
        self.qtgui_vector_sink_f_0.enable_autoscale(False)
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
        self.phase_04 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.phase_04.set_update_time(0.10)
        self.phase_04.set_title("")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.phase_04.set_min(i, -1)
            self.phase_04.set_max(i, 1)
            self.phase_04.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.phase_04.set_label(i, "Data {0}".format(i))
            else:
                self.phase_04.set_label(i, labels[i])
            self.phase_04.set_unit(i, units[i])
            self.phase_04.set_factor(i, factor[i])

        self.phase_04.enable_autoscale(False)
        self._phase_04_win = sip.wrapinstance(self.phase_04.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._phase_04_win)
        self.phase_03 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.phase_03.set_update_time(0.10)
        self.phase_03.set_title("")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.phase_03.set_min(i, -1)
            self.phase_03.set_max(i, 1)
            self.phase_03.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.phase_03.set_label(i, "Data {0}".format(i))
            else:
                self.phase_03.set_label(i, labels[i])
            self.phase_03.set_unit(i, units[i])
            self.phase_03.set_factor(i, factor[i])

        self.phase_03.enable_autoscale(False)
        self._phase_03_win = sip.wrapinstance(self.phase_03.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._phase_03_win)
        self.phase_02 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.phase_02.set_update_time(0.10)
        self.phase_02.set_title("")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.phase_02.set_min(i, -1)
            self.phase_02.set_max(i, 1)
            self.phase_02.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.phase_02.set_label(i, "Data {0}".format(i))
            else:
                self.phase_02.set_label(i, labels[i])
            self.phase_02.set_unit(i, units[i])
            self.phase_02.set_factor(i, factor[i])

        self.phase_02.enable_autoscale(False)
        self._phase_02_win = sip.wrapinstance(self.phase_02.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._phase_02_win)
        self.phase_01 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.phase_01.set_update_time(0.10)
        self.phase_01.set_title("")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.phase_01.set_min(i, -1)
            self.phase_01.set_max(i, 1)
            self.phase_01.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.phase_01.set_label(i, "Data {0}".format(i))
            else:
                self.phase_01.set_label(i, labels[i])
            self.phase_01.set_unit(i, units[i])
            self.phase_01.set_factor(i, factor[i])

        self.phase_01.enable_autoscale(False)
        self._phase_01_win = sip.wrapinstance(self.phase_01.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._phase_01_win)
        self.krakensdr_krakensdr_source_0 = krakensdr.krakensdr_source('127.0.0.1', 5000, 5001, 1048576, 5, freq, [30, 30, 30, 30, 30], False)
        self.krakensdr_krakensdr_correlator_0_0_1 = krakensdr.krakensdr_correlator(vec_len, fft_cut)
        self.krakensdr_krakensdr_correlator_0_0_0 = krakensdr.krakensdr_correlator(vec_len, fft_cut)
        self.krakensdr_krakensdr_correlator_0_0 = krakensdr.krakensdr_correlator(vec_len, fft_cut)
        self.krakensdr_krakensdr_correlator_0 = krakensdr.krakensdr_correlator(vec_len, fft_cut)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.krakensdr_krakensdr_correlator_0, 1), (self.phase_01, 0))
        self.connect((self.krakensdr_krakensdr_correlator_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.krakensdr_krakensdr_correlator_0_0, 1), (self.phase_02, 0))
        self.connect((self.krakensdr_krakensdr_correlator_0_0, 0), (self.qtgui_vector_sink_f_0_0, 0))
        self.connect((self.krakensdr_krakensdr_correlator_0_0_0, 1), (self.phase_03, 0))
        self.connect((self.krakensdr_krakensdr_correlator_0_0_0, 0), (self.qtgui_vector_sink_f_0_0_0, 0))
        self.connect((self.krakensdr_krakensdr_correlator_0_0_1, 1), (self.phase_04, 0))
        self.connect((self.krakensdr_krakensdr_correlator_0_0_1, 0), (self.qtgui_vector_sink_f_0_0_0_0, 0))
        self.connect((self.krakensdr_krakensdr_source_0, 1), (self.krakensdr_krakensdr_correlator_0, 1))
        self.connect((self.krakensdr_krakensdr_source_0, 0), (self.krakensdr_krakensdr_correlator_0, 0))
        self.connect((self.krakensdr_krakensdr_source_0, 2), (self.krakensdr_krakensdr_correlator_0_0, 1))
        self.connect((self.krakensdr_krakensdr_source_0, 0), (self.krakensdr_krakensdr_correlator_0_0, 0))
        self.connect((self.krakensdr_krakensdr_source_0, 3), (self.krakensdr_krakensdr_correlator_0_0_0, 1))
        self.connect((self.krakensdr_krakensdr_source_0, 0), (self.krakensdr_krakensdr_correlator_0_0_0, 0))
        self.connect((self.krakensdr_krakensdr_source_0, 0), (self.krakensdr_krakensdr_correlator_0_0_1, 0))
        self.connect((self.krakensdr_krakensdr_source_0, 4), (self.krakensdr_krakensdr_correlator_0_0_1, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "kraken_corr_test")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_vec_len(self):
        return self.vec_len

    def set_vec_len(self, vec_len):
        self.vec_len = vec_len

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        Qt.QMetaObject.invokeMethod(self._freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.freq)))
        self.krakensdr_krakensdr_source_0.set_freq(self.freq)

    def get_fft_cut(self):
        return self.fft_cut

    def set_fft_cut(self, fft_cut):
        self.fft_cut = fft_cut




def main(top_block_cls=kraken_corr_test, options=None):

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
