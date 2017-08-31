import numpy as np
from gainData import AntennaBalunMeasurement as ABM
from gainData import AntennaDiffMeasurement as ADM
from gainData import GainData as GD
import matplotlib.pyplot as plt

n_measurements=6
#measurement_names=['_balun_b_%d_'%m for m in range(2,n_measurements+1)]
measurement_names=['_balun_b_%d_'%m for m in [4,5,6]]
labels=['0clicks','4clicks','2clicks']
colors=['black','grey','red']

simulation=GD()
simulation.read_files('../August30thSinuousFeedOverDish/Simulation/S11_0.80-30-175_dish-imp-100-band_no-skirt-1.2-0.3-backplane-50-0.99','CST_S11',fMin=0.05,fMax=0.25)
simulation.gainFrequency=simulation.gainFrequency
db_s11_sim=10.*np.log10(np.abs(simulation.gainFrequency))
pha_s11_sim=np.angle(simulation.gainFrequency)

fig1=plt.figure()
fig2=plt.figure()
ax1=fig1.add_axes([.1,.1,.8,.8])
ax2=fig2.add_axes([.1,.1,.8,.8])

for fnum,fname in enumerate(measurement_names):
    hybrid_coupler_B=ABM()
    hybrid_coupler_B.read_files('../August30thSinuousFeedOverDish/',fname,
                                '../hybrid_coupler_B/1','_','ANRITSU_CSV',
                                '1','3','4',0.05,0.25)
    db_s11_B_corr=10.*np.log10(np.abs(hybrid_coupler_B.antenna_gain_frequency))
    db_s11_B=10.*np.log10(np.abs(hybrid_coupler_B.antenna_raw.gainFrequency))
    pha_s11_B_corr=np.angle(hybrid_coupler_B.antenna_gain_frequency)
    pha_s11_B=np.angle(hybrid_coupler_B.antenna_raw.gainFrequency)

    ax1.plot(hybrid_coupler_B.fAxis,db_s11_B,color=colors[fnum],ls='--',alpha=.75)
    ax1.plot(hybrid_coupler_B.fAxis,db_s11_B_corr,color=colors[fnum],label=labels[fnum])
    ax2.plot(hybrid_coupler_B.fAxis,pha_s11_B,color=colors[fnum],ls='--',alpha=.5)
    ax2.plot(hybrid_coupler_B.fAxis,pha_s11_B_corr,color=colors[fnum],label='Balun B Corrected')


ax1.plot(simulation.fAxis,db_s11_sim,color='k',lw=5,label='Simulation')
ax1.grid()
fig1.set_size_inches(10,6)
ax1.set_xlabel('frequency (GHz)')
ax1.set_ylabel('|S$_{11}$| (dB)')
ax1.legend(loc='best')
ax2.plot(simulation.fAxis,pha_s11_sim,color='k',lw=5,label='Simulation')
ax2.grid()
fig2.set_size_inches(10,6)
ax2.set_xlabel('frequency (GHz)')
ax2.set_ylabel('Arg($S_{11}$) (rad)')
ax2.legend(loc='best')

fig1.savefig('Sinuous_s11_amp_comarision_August_30th_2017.pdf')
fig2.savefig('Sinuous_s11_pha_comarision_August_30th_2017.pdf')


plt.show()
