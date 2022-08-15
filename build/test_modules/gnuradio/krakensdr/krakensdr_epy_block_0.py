"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block - Used to output phase information from KrakenSDR when noise source is forced always ON."""

    def __init__(self, vec_len=2**20):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Phase at Zero in Degrees',   # will show up in GRC
            in_sig=[(np.complex64, vec_len)],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.vec_len = vec_len

    def work(self, input_items, output_items):        
        input_0 = np.empty(self.vec_len, dtype=np.complex64)
        input_0 = input_items[0][0]

        phase = np.rad2deg(np.angle(input_0[0]))

        output_items[0][:] = phase
        return len(output_items[0])
