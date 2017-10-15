#!/bin/bash
source activate hera_antenna
python plot_measurements_config.py --input compare_sinuous_impedance.conf --output compare_sinuous_impedance_delay --domain delay --fmin -0.05 --fmax 0.25
python plot_measurements_config.py --input compare_sinuous_impedance.conf --output compare_sinuous_impedance_freq --domain freq --fmin 0.05 --fmax 0.25 -m -20 -x 3
