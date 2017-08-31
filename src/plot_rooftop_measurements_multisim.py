import numpy as np
from gainData import AntennaBalunMeasurement as ABM
from gainData import AntennaDiffMeasurement as ADM
from gainData import GainData as GD
import matplotlib.pyplot as plt

#load measurements
hybrid_coupler_A=ABM()
hybrid_coupler_B=ABM()
cambridge_balun=ABM()
no_balun=ADM()

hybrid_coupler_A.read_files('../Rooftop_Antenna_Measurements_August_10th/','_hybrid_A_port_A_antenna_',
                            '../hybrid_coupler_A_Sierra/A_','_','ANRITSU_CSV',
                            '1','3','4',0.05,0.25)
hybrid_coupler_B.read_files('../Rooftop_Antenna_Measurements_August_10th/','_hybrid_B_port_A_antenna_',
                            '../hybrid_coupler_B/1','_','ANRITSU_CSV',
                            '1','3','4',0.05,0.25)
cambridge_balun.read_files('../Rooftop_Antenna_Measurements_August_10th/','_cambridge_balun_N_antenna_0_',
                            '../Cambridge_Balun_Measurements_N/','_','ANRITSU_CSV',
                            '1','2','3',0.05,0.25)

no_balun.read_files('../Rooftop_Antenna_Measurements_August_10th/','_no_balun_antenna_','ANRITSU_CSV',0.05,0.25)

dists=[30,50,70]
simulationnames=['../Rooftop_Antenna_Measurements_August_10th/Simulation/Backplane Adjustment/S11_0.80-30-175_no-imp-100-band-no-skirt-1.2-0.3-backplane-%d-0.99'%(dist) for dist in dists]

fig1=plt.figure()
fig2=plt.figure()


ax1=fig1.add_axes([.1,.1,.8,.8])
ax2=fig2.add_axes([.1,.1,.8,.8])

colors=['black','red','orange']

for simnum,simname in enumerate(simulationnames):
    simulation=GD()
    simulation.read_files(simname,'CST_S11',fMin=0.05,fMax=0.25)
    simulation.gainFrequency=simulation.gainFrequency
    db_s11_sim=10.*np.log10(np.abs(simulation.gainFrequency))
    pha_s11_sim=np.angle(simulation.gainFrequency)
    ax1.plot(simulation.fAxis,db_s11_sim,lw=5,label='Simulation, h=%dcm'%(dists[simnum]),color=colors[simnum])
    ax2.plot(simulation.fAxis,pha_s11_sim,lw=5,label='Simulation,h=%dcm'%(dists[simnum]),color=colors[simnum])




db_s11_A_corr=10.*np.log10(np.abs(hybrid_coupler_A.antenna_gain_frequency))
db_s11_A=10.*np.log10(np.abs(hybrid_coupler_A.antenna_raw.gainFrequency))
db_s11_B_corr=10.*np.log10(np.abs(hybrid_coupler_B.antenna_gain_frequency))
db_s11_B=10.*np.log10(np.abs(hybrid_coupler_B.antenna_raw.gainFrequency))
db_s11_cam_corr=10.*np.log10(np.abs(cambridge_balun.antenna_gain_frequency))
db_s11_cam=10.*np.log10(np.abs(cambridge_balun.antenna_raw.gainFrequency))
db_s11_no_balun=10.*np.log10(np.abs(no_balun.antenna_gain_frequency))



pha_s11_A_corr=np.angle(hybrid_coupler_A.antenna_gain_frequency)
pha_s11_A=np.angle(hybrid_coupler_A.antenna_raw.gainFrequency)
pha_s11_B_corr=np.angle(hybrid_coupler_B.antenna_gain_frequency)
pha_s11_B=np.angle(hybrid_coupler_B.antenna_raw.gainFrequency)
pha_s11_cam_corr=np.angle(cambridge_balun.antenna_gain_frequency)
pha_s11_cam=np.angle(cambridge_balun.antenna_raw.gainFrequency)
pha_s11_no_balun=np.angle(no_balun.antenna_gain_frequency)



ax1.plot(hybrid_coupler_A.fAxis,db_s11_A,color='k',ls='--',alpha=.5)
ax1.plot(hybrid_coupler_A.fAxis,db_s11_A_corr,color='k',label='Balun A Corrected',marker='x')
#ax1.plot(hybrid_coupler_B.fAxis,db_s11_B,color='grey',ls='--',alpha=.5)
#ax1.plot(hybrid_coupler_B.fAxis,db_s11_B_corr,color='grey',label='Balun B Corrected')
#ax1.plot(cambridge_balun.fAxis,db_s11_cam,color='red',ls='--',alpha=.5)
#ax1.plot(cambridge_balun.fAxis,db_s11_cam_corr,color='red',label='Balun C Corrected')
#ax1.plot(no_balun.fAxis,db_s11_no_balun,color='orange',label='No Balun')
ax1.grid()
fig1.set_size_inches(10,6)
ax1.set_xlabel('frequency (GHz)')
ax1.set_ylabel('|S$_{11}$| (dB)')
ax1.legend(loc='best')

plotstrs=['s11','s1d','sd1','sdd','s1c','sc1','scc','scd','sdc']

ax2.plot(hybrid_coupler_A.fAxis,pha_s11_A,color='k',ls='--',alpha=.5)
ax2.plot(hybrid_coupler_A.fAxis,pha_s11_A_corr,color='k',label='Balun A Corrected')
#ax2.plot(hybrid_coupler_B.fAxis,pha_s11_B,color='grey',ls='--',alpha=.5)
#ax2.plot(hybrid_coupler_B.fAxis,pha_s11_B_corr,color='grey',label='Balun B Corrected')
#ax2.plot(cambridge_balun.fAxis,pha_s11_cam,color='red',ls='--',alpha=.5)
#ax2.plot(cambridge_balun.fAxis,pha_s11_cam_corr,color='red',label='Balun C Corrected')
#ax2.plot(no_balun.fAxis,pha_s11_no_balun,color='orange',label='No Balun')
ax2.grid()
fig2.set_size_inches(10,6)
ax2.set_xlabel('frequency (GHz)')
ax2.set_ylabel('Arg($S_{11}$) (rad)')
ax2.legend(loc='best')



fig1.savefig('Sinuous_s11_amp_comarision_August_10th_2017_simulations.pdf')
fig2.savefig('Sinuous_s11_pha_comarision_August_10th_2017_simulations.pdf')


plt.show()
