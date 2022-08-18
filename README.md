# KrakenSDR GNU Radio Source Block
This is a GNU Radio Block for KrakenSDR. It connects via a TCP socket connection to the KrakenSDR DAQ server software called Heimdall. Heimdall handles all sample and phase coherence calibration via the noise source, and this block receives the coherent IQ sample output and makes it available for further DSP processing in GNU Radio.

<img src="https://user-images.githubusercontent.com/78108016/185366866-f0784cc1-4a8c-4140-add5-88c271c7494c.png" width="250">
<img src="https://user-images.githubusercontent.com/78108016/185367619-2c9baa15-186e-4b11-9133-d6cf80f53608.png" width="500">

## GNU Radio OOT Block Install Instructions

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

## Usage Instructions

First install Heimdall https://github.com/krakenrf/heimdall_daq_fw

Next copy the heimdall_only_start.sh file from this repo into your krakensdr root directory.

In the heimdall_daq_fw folder edit your Firmware/daq_chain_config.ini file and change out_data_iface_type to eth.

```
[data_interface]
out_data_iface_type = eth
```

Then in the krakensdr root directory run ./heimdall_only_start.sh

Now you can start your GRC file with the KrakenSDR source, and it will make a socket connection to the heimdall code at IP 127.0.0.1. Alternatively, you can run the heimdall code on a networked device, but you will need a fast Gigabit and possibly direct network connection to ensure the network throughput is sufficient to handle the five channels.

### FFT Test
Included in the examples folder is a simple example grc file called 'kraken_fft_display.grc'. This will display the FFT of the 5-channels.

![krakensdr_gnuradio_fft](https://user-images.githubusercontent.com/78108016/185366658-aaceb80a-c4a2-41cb-a1f7-770fa6007b48.png)

### DOA MUSIC
There is also a direction finding example file called 'kraken_music_doa.grc'. This can be used for radio direction finding and it makes use of the MUSIC algorithm.

![krakensdr_gnuradio_music_doa](https://user-images.githubusercontent.com/78108016/185367262-217cebea-b907-493d-9867-c60000f3dcef.png)

### Correlation Check
Also included is a cross correlator block called 'kraken_correlator_test' can be used to check for sample and phase coherence via cross correlating each channel against channel zero. To test this block you'll need to slightly modify the heimdall core code to make the noise source stay on constantly. Edit the Firmware/_daq_core/rtl_daq.c file with a text editor, and near the end of the file change the last zero in rtlsdr_set_bias_tee_gpio to a '1'. Then in the Firmware/_daq_core folder run 'make'. Be sure to revert this edit and run make again when you're done.

```
else if (noise_source_state == 0){
    //rtlsdr_set_bias_tee_gpio(rtl_rec->dev, 0, 0);
    rtlsdr_set_bias_tee_gpio(rtl_rec->dev, 0, 1);
```    

![krakensdr_gnuradio_cross_correlator](https://user-images.githubusercontent.com/78108016/185367575-6c49cc38-a996-4850-9162-740227e2bb0d.png)
