#!/bin/bash
source activate hera_antenna
#python plot_measurements_config.py -i compare_FEM_timetraces.conf -d delay -n True -l 0.05 -u 0.25 -o compare_fem_simulations_fullband
python plot_measurements_config.py -i compare_FEM_timetraces.conf -d delay -n True -l 0.1 -u 0.2 -o compare_fem_simulations_heraband -t "100 to 200MHz"
python plot_measurements_config.py -i compare_FEM_timetraces.conf -d delay -n True -l 0.17 -u 0.2 -o compare_fem_simulations_herahighband -t "170 to 200MHz"
python plot_measurements_config.py -i compare_FEM_timetraces.conf -d delay -n True -l 0.14 -u 0.17 -o compare_fem_simulations_heramidband -t "140 to 170MHz"
python plot_measurements_config.py -i compare_FEM_timetraces.conf -d delay -n True -l 0.11 -u 0.14 -o compare_fem_simulations_heralowband -t "110 to 130MHz"
python plot_measurements_config.py -i compare_FEM_timetraces.conf -d delay -n True -l 0.1 -u 0.14 -o compare_fem_simulations_heraband1 -t "100 to 140MHz"
python plot_measurements_config.py -i compare_FEM_timetraces.conf -d delay -n True -l 0.11 -u 0.15 -o compare_fem_simulations_heraband2 -t "110 to 150MHz"
python plot_measurements_config.py -i compare_FEM_timetraces.conf -d delay -n True -l 0.12 -u 0.16 -o compare_fem_simulations_heraband3 -t "120 to 160MHz"
python plot_measurements_config.py -i compare_FEM_timetraces.conf -d delay -n True -l 0.13 -u 0.17 -o compare_fem_simulations_heraband4 -t "130 to 170MHz"
python plot_measurements_config.py -i compare_FEM_timetraces.conf -d delay -n True -l 0.14 -u 0.18 -o compare_fem_simulations_heraband5 -t "140 to 180MHz"
python plot_measurements_config.py -i compare_FEM_timetraces.conf -d delay -n True -l 0.15 -u 0.19 -o compare_fem_simulations_heraband5 -t "150 to 190MHz"
python plot_measurements_config.py -i compare_FEM_timetraces.conf -d delay -n True -l 0.16 -u 0.2 -o compare_fem_simulations_heraband5 -t "160 to 200MHz"
