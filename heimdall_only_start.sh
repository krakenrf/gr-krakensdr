#!/bin/bash

#source /home/krakenrf/miniforge3/etc/profile.d/conda.sh <- required for systemd auto startup (comment out eval and use source instead)
eval "$(conda shell.bash hook)"
conda activate kraken

./heimdall_only_stop.sh
sleep 2

cd heimdall_daq_fw/Firmware
sudo env "PATH=$PATH" ./daq_start_sm.sh
