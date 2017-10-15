#!/bin/bash
source activate hera_antenna
plotdir=/Users/ewallwic/Dropbox_MIT/Science/simulations-hera-eox/analysis/
#python plot_measurements_config.py -i compare_FEM_timetraces.conf -d delay -n True -l 0.05 -u 0.25 -o compare_fem_simulations_fullband
python plot_measurements_config.py -i compare_FEM_timetraces.conf -d delay -n True -l 0.1 -u 0.2 -o compare_fem_simulations_heraband -t "100 to 200MHz" -o ${plotdir}planewave_delay_FEM.png
python plot_measurements_config.py -i compare_FEM_timetraces.conf -d delay -n True -l 0.17 -u 0.2 -o compare_fem_simulations_herahighband -t "50 to 120MHz" -o ${plotdir}planewave_delay_100Ohm.png
