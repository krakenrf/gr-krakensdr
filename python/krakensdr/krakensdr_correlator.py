#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 KrakenRF Inc.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr

class krakensdr_correlator(gr.sync_block):
    """
    docstring for block krakensdr_correlator
    """
    def __init__(self, vec_len=2**20, fft_cut=2048):
        gr.sync_block.__init__(self,
            name='Correlation Sample and Phase',   # will show up in GRC
            in_sig=[(np.complex64, vec_len), (np.complex64, vec_len)],
            out_sig=[(np.float32, fft_cut), np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.vec_len = vec_len
        self.fft_cut = fft_cut

    def work(self, input_items, output_items):
        try:
            # Do correlation in the FFT domain and output correlation plot and calculated phase
            # If samples are correlated, the peak will be centered, and is phase is calibrated, it will be near zero.
            iq_samples_0 = np.empty(self.vec_len, dtype=np.complex64)
            iq_samples_0 = input_items[0][0]
            iq_samples_1 = np.empty(self.vec_len, dtype=np.complex64)
            iq_samples_1 = input_items[1][0]

            N = self.vec_len
            np_zeros = np.zeros(N, dtype=np.complex64)
            x_padd = np.concatenate([iq_samples_0, np_zeros])
            x_fft = np.fft.fft(x_padd)

            y_padd = np.concatenate([np_zeros, iq_samples_1])
            y_fft = np.fft.fft(y_padd)

            x_corr = np.fft.ifft(x_fft.conj() * y_fft)
            x_corr_plot = 10*np.log10(np.abs(x_corr))
            x_corr_plot -= np.max(x_corr_plot)

            M = self.fft_cut // 2
            x_corr_plot = x_corr_plot[N-M:N+M]

            phase = np.rad2deg(np.angle(x_corr[N]))

            if not np.isnan(x_corr_plot).any():
                output_items[0][:] = x_corr_plot
                output_items[1][:] = phase
        except:
            pass

        return len(output_items[0])
