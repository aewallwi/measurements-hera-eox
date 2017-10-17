#!/bin/bash
source activate hera_antenna
#python plot_measurements_config.py -i compare_FEM_timetraces.conf -d freq -n True -l 0.05 -u 0.25 -o compare_fem_simulations_fullband
python plot_measurements_config.py -i compare_FEM_s11.conf -d freq -l 0.05 -u 0.25 -o compare_s11_mixed_impedances -t "050 to 250MHz" -m -15 -x 3
