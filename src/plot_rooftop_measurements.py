import numpy as np
from gainData import AntennaBalunMeasurement as AM
import gainData as GD
import matplotlib.pyplot as plt

#load measurements
hybrid_coupler_A=AM()
hybrid_coupler_A.read_files('../Rooftop_Antenna_Measurements_August_10th/','_hybrid_A_port_A_antenna',
                            '../hybrid_coupler_A_Sierra/A_','','ANRITSU_CSV',
                            '1','3','4',0.05,0.25)
#load Jianshu's data

db_s11_corr=10.*np.log10(np.abs(hybrid_coupler_A.antenna_gain_corrected_frequency))
db_s11=10.*np.log10(np.abs(hybrid_coupler_A.antenna_raw.gainFrequency))

fig1=plt.figure()
fig2=plt.figure()
ax1=fig1.add_axes([.1,.1,.8,.8])
ax2=fig2.add_axes([.1,.1,.8,.8])



ax1.plot(hybrid_coupler_A.fAxis,db_s11)
ax1.plot(hybrid_coupler_A.fAxis,db_s11_corr)

plotstrs=['s11','s1d','sd1','sdd','s1c','sc1','scc','scd','sdc']
plotstrs=['s11','s12','s13','s21','s22','s23','s31','s32','s33']
#plotstrs=['s11']
for dstring in plotstrs:
    print dstring
    y=np.abs(hybrid_coupler_A.balun.get_ss(dstring))
    print y
    y=10.*np.log10(y)
    x=hybrid_coupler_A.balun.fAxis
    ax2.plot(x,y,label=dstring)
ax2.legend(loc='best')
    

plt.show()
