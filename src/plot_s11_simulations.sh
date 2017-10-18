#!/bin/bash
source activate hera_antenna
odir=/Users/ewallwic/Dropbox_MIT/Science/simulations-hera-eox/analysis/downselect_plots/s11_freq

#python plot_measurements_config.py -i compare_FEM_timetraces.conf -d freq -n True -l 0.05 -u 0.25 -o compare_fem_simulations_fullband
python plot_measurements_config.py -i compare_FEM_s11.conf -d freq -l 0.05 -u 0.24 -o ${odir}compare_s11_mixed_impedances_FEM -t "050 to 250MHz FEM Termination" -m -15 -x 3
python plot_measurements_config.py -i compare_100Ohm_s11.conf -d freq -l 0.05 -u 0.24 -o ${odir}compare_s11_mixed_impedances_100Ohm -t "050 to 250MHz 100 Ohm Termination" -m -15 -x 3

odir=/Users/ewallwic/Dropbox_MIT/Science/simulations-hera-eox/analysis/downselect_plots/s11_delay

python plot_measurements_config.py -i compare_FEM_s11.conf -d delay -l 0.05 -u 0.25 -o ${odir}compare_s11_mixed_impedances_FEM_delay -t "050 to 250MHz FEM Termination"
python plot_measurements_config.py -i compare_100Ohm_s11.conf -d delay -l 0.05 -u 0.25 -o ${odir}compare_s11_mixed_impedances_100Ohm_delay -t "050 to 250MHz 100 Ohm Termination" 

python plot_measurements_config.py -i compare_FEM_s11_low.conf -d delay -l 0.05 -u 0.12 -o ${odir}compare_s11_mixed_impedances_low_FEM_delay -t "050 to 100MHz FEM Termination"

python plot_measurements_config.py -i compare_100Ohm_s11_low.conf -d delay -l 0.05 -u 0.12 -o ${odir}compare_s11_mixed_impedances_low_100Ohm_delay -t "050 to 100MHz 100 Ohm Termination"



python plot_measurements_config.py -i compare_100Ohm_s11_high.conf -d delay -l 0.1 -u 0.2 -o ${odir}compare_s11_mixed_impedances_high_100Ohm_delay -t "100 to 200 MHz 100 Ohm Termination" 

python plot_measurements_config.py -i compare_FEM_s11_high.conf -d delay -l 0.1 -u 0.2 -o ${odir}compare_s11_mixed_impedances_high_FEM_delay -t "100 to 200 MHz FEM Termination"
