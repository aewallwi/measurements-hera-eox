#!/bin/bash
source activate hera_antenna
plotdir=/Users/ewallwic/Dropbox_MIT/Science/simulations-hera-eox/analysis/downselect_plots/
python plot_measurements_config.py -i compare_100Ohm_timetraces_low_noconv.conf -d delay -n True -l 0.05 -u 0.12 -t "50 to 120MHz" -o ${plotdir}kernel_FEM_lowband -z True -k True
python plot_measurements_config.py -i compare_FEM_timetraces_low_noconv.conf -d delay -n True -l 0.05 -u 0.12 -t "50 to 120MHz" -o ${p_lotdir}planewave_delay_FEM_lowband -z True -k True

#python plot_measurements_config.py -i compare_100Ohm_timetraces_high.conf -d delay -n True -l 0.1 -u 0.2 -t "100 to 200MHz" -o ${plotdir}planewave_delay_100Ohm_highband -z True
#python plot_measurements_config.py -i compare_100Ohm_timetraces_low.conf -d delay -n True -l 0.05 -u 0.12  -t "50 to 120MHz" -o ${plotdir}planewave_delay_100Ohm_lowband -z True

