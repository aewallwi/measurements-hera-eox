#************************************************************************
#compare simulations of full and partial band sinuous antenna time traces
#************************************************************************
#!/bin/bash
source activate hera_antenna
python plot_measurements_config.py -i compare_sinuous_simulations.conf -d delay --fmin 0.05 --fmax 0.25 --output compare_sinuous_fullband
