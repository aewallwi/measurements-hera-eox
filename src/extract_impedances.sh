#!/bin/bash
#script to extract impedances from
zdir=/Users/ewallwic/Dropbox_MIT/Science/simulations-hera-eox/data/impedances/
source activate hera_antenna
sdir=/Users/ewallwic/Dropbox_MIT/Science/simulations-hera-eox/data/sParameters/
#start with extracting the FEM from z11 and s11 of vivaldi
python extract_impedance.py -s ${sdir}Differential_S11_Vivaldi_1.3m_FEM -z ${zdir}Differential_ant_imp_Vivaldi_1.3m.z1p -a True -f CST_S11 -l 0.05 -u 0.25 -o ${zdir}/FEM.z1p

