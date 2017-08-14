import numpy as np
from gainData import AntennaBalunMeasurement as AM
import gainData as GD
import matplotlib.pyplot as plt

#load measurements
hybrid_coupler_A=AM()
hybrid_coupler_A.read_files('../Rooftop_Antenna_Measurements_August_10th/','_hybrid_A_port_A_antenna',
                            '../hybrid_coupler_A_Sierra/A_','','ANRITSU_CSV',
                            '1','2','3',0.05,0.25)
#load Jianshu's data

db_s11_corr=10.*np.log10(np.abs(hybrid_coupler_A.antenna_gain_corrected_frequency))
db_s11=10.*np.log10(np.abs(hybrid_coupler_A.antenna_raw.gainFrequency))
plt.plot(hybrid_coupler_A.fAxis,db_s11)
plt.plot(hybrid_coupler_A.fAxis,db_s11_corr)
plt.show()
