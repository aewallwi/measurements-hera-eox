#!/bin/bash
#script to extract impedances from
zdir=/Users/ewallwic/Dropbox_MIT/Science/simulations-hera-eox/data/impedances/
source activate hera_antenna
sdir=/Users/ewallwic/Dropbox_MIT/Science/simulations-hera-eox/data/sParameters/
#start with extracting the FEM from z11 and s11 of vivaldi
python extract_impedance.py -s ${sdir}S11_Vivaldi_1.3m-ref_100_ohm.s1p -z 100 -f S11_S1P -l 0.05 -u 0.25 -o ${zdir}/Vivaldi_1.3m.z1p
python extract_impedance.py -s ${sdir}S11_Vivaldi_1.7m-ref_100_ohm.s1p -z 100 -f S11_S1P -l 0.05 -u 0.25 -o ${zdir}/Vivaldi_1.7m.z1p
python extract_impedance.py -s ${sdir}S11_Sinuous-ref_100_ohm.s1p -z 100 -f S11_S1P -l 0.05 -u 0.25 -o ${zdir}/Sinuous_gr0.5_bp90cm.z1p
python extract_impedance.py -s ${sdir}S11_CTP-ref_100_ohm.s1p -z 100 -f S11_S1P -l 0.05 -u 0.25 -o ${zdir}/CTP_1.9m_tall.z1p
python extract_impedance.py -s ${sdir}HERA_feed_high_with_dish_5m.s2p -z 100 -f S11_S1P -l 0.05 -u 0.25 -o ${zdir}/convertible_high.z1p
python extract_impedance.py -s ${sdir}HERA_feed_low_with_dish_5m.s2p -z 100 -f S11_S1P -l 0.05 -u 0.25 -o ${zdir}/convertible_low.z1pS
python extract_impedance.py -s ${sdir}S11_HERA-ref_100_ohm.s1p -z 100 -f S11_S1P -l 0.05 -u 0.25 -o ${zdir}/highband.z1p
