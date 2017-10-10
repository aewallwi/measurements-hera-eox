#!/bin/bash
source activate hera_antenna
python plot_measurements_config.py -i compare_FEM_timetraces.conf -d delay -n True -l 0.05 -u 0.25 -o compare_fem_simulations_fullband.png
