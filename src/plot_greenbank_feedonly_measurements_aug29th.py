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

hybrid_coupler_A.read_files('../August29thFeedOnlySinuous/','_a_',
                            '../hybrid_coupler_A_Sierra/A_','_','ANRITSU_CSV',
                            '1','3','4',0.05,0.25)
hybrid_coupler_B.read_files('../August29thFeedOnlySinuous/','_b_',
                            '../hybrid_coupler_B/1','_','ANRITSU_CSV',
                            '1','3','4',0.05,0.25)
#cambridge_balun.read_files('../GreenBankMeasurements_FeedOnly_August_28th_2017/','_30-175-0.8-230-0.99-50-C-',
#                            '../Cambridge_Balun_Measurements_N/','_','ANRITSU_CSV',
#                            '1','2','3',0.05,0.25)

no_balun.read_files('../August29thFeedOnlySinuous/','_no_','ANRITSU_CSV',0.05,0.25)

simulation=GD()
simulation.read_files('../Rooftop_Antenna_Measurements_August_10th/Simulation/simulation_s11_rooftop','CST_S11',fMin=0.05,fMax=0.25)
simulation.gainFrequency=simulation.gainFrequency

#load Jianshu's data
'''
impedance_sim_amp=np.loadtxt(('../Rooftop_Antenna_Measurements_August_10th/'
                              'Simulation/simulation_impedance_rooftop_amp.txt'))
impedance_sim_pha=np.loadtxt(('../Rooftop_Antenna_Measurements_August_10th/'
                              'Simulation/simulation_impedance_rooftop_pha.txt'))
sim_impedance=impedance_sim_amp[:,1]*np.exp(1j*impedance_sim_pha[:,1])
sim_freq=impedance_sim_amp[:,0]
sim_s11=(sim_impedance-100)/(sim_impedance+100)
fig0=plt.figure()
ax0=fig0.add_axes([.1,.1,.8,.8])
ax0.plot(sim_impedance.real)
ax0.plot(sim_impedance.imag)
'''


db_s11_A_corr=10.*np.log10(np.abs(hybrid_coupler_A.antenna_gain_frequency))
db_s11_A=10.*np.log10(np.abs(hybrid_coupler_A.antenna_raw.gainFrequency))
db_s11_B_corr=10.*np.log10(np.abs(hybrid_coupler_B.antenna_gain_frequency))
db_s11_B=10.*np.log10(np.abs(hybrid_coupler_B.antenna_raw.gainFrequency))
#db_s11_cam_corr=10.*np.log10(np.abs(cambridge_balun.antenna_gain_frequency))
#db_s11_cam=10.*np.log10(np.abs(cambridge_balun.antenna_raw.gainFrequency))
db_s11_no_balun=10.*np.log10(np.abs(no_balun.antenna_gain_frequency))
db_s11_sim=10.*np.log10(np.abs(simulation.gainFrequency))



pha_s11_A_corr=np.angle(hybrid_coupler_A.antenna_gain_frequency)
pha_s11_A=np.angle(hybrid_coupler_A.antenna_raw.gainFrequency)
pha_s11_B_corr=np.angle(hybrid_coupler_B.antenna_gain_frequency)
pha_s11_B=np.angle(hybrid_coupler_B.antenna_raw.gainFrequency)
#pha_s11_cam_corr=np.angle(cambridge_balun.antenna_gain_frequency)
#pha_s11_cam=np.angle(cambridge_balun.antenna_raw.gainFrequency)
pha_s11_no_balun=np.angle(no_balun.antenna_gain_frequency)
pha_s11_sim=np.angle(simulation.gainFrequency)

fig1=plt.figure()
fig2=plt.figure()
#fig3=plt.figure()
#fig4=plt.figure()

ax1=fig1.add_axes([.1,.1,.8,.8])
ax2=fig2.add_axes([.1,.1,.8,.8])
#ax3=fig3.add_axes([.1,.1,.8,.8])
#ax4=fig4.add_axes([.1,.1,.8,.8])

ax1.plot(hybrid_coupler_A.fAxis,db_s11_A,color='k',ls='--',alpha=.75)
ax1.plot(hybrid_coupler_A.fAxis,db_s11_A_corr,color='k',label='Balun A Corrected')
ax1.plot(hybrid_coupler_B.fAxis,db_s11_B,color='grey',ls='--',alpha=.75)
ax1.plot(hybrid_coupler_B.fAxis,db_s11_B_corr,color='grey',label='Balun B Corrected')
#ax1.plot(cambridge_balun.fAxis,db_s11_cam,color='red',ls='--',alpha=.5)
#ax1.plot(cambridge_balun.fAxis,db_s11_cam_corr,color='red',label='Balun C Corrected')
ax1.plot(no_balun.fAxis,db_s11_no_balun,color='orange',label='No Balun')
ax1.plot(simulation.fAxis,db_s11_sim,color='k',lw=5,label='Simulation')
ax1.grid()
fig1.set_size_inches(10,6)
ax1.set_xlabel('frequency (GHz)')
ax1.set_ylabel('|S$_{11}$| (dB)')
ax1.legend(loc='best')

plotstrs=['s11','s1d','sd1','sdd','s1c','sc1','scc','scd','sdc']

ax2.plot(hybrid_coupler_A.fAxis,pha_s11_A,color='k',ls='--',alpha=.5)
ax2.plot(hybrid_coupler_A.fAxis,pha_s11_A_corr,color='k',label='Balun A Corrected')
ax2.plot(hybrid_coupler_B.fAxis,pha_s11_B,color='grey',ls='--',alpha=.5)
ax2.plot(hybrid_coupler_B.fAxis,pha_s11_B_corr,color='grey',label='Balun B Corrected')
#ax2.plot(cambridge_balun.fAxis,pha_s11_cam,color='red',ls='--',alpha=.5)
#ax2.plot(cambridge_balun.fAxis,pha_s11_cam_corr,color='red',label='Balun C Corrected')
ax2.plot(no_balun.fAxis,pha_s11_no_balun,color='orange',label='No Balun')
ax2.plot(simulation.fAxis,pha_s11_sim,color='k',lw=5,label='Simulation')
ax2.grid()
fig2.set_size_inches(10,6)
ax2.set_xlabel('frequency (GHz)')
ax2.set_ylabel('Arg($S_{11}$) (rad)')
ax2.legend(loc='best')


#ax3.plot(hybrid_coupler_A.fAxis,hybrid_coupler_A.antenna_gain_frequency.real,color='k')
#ax3.plot(hybrid_coupler_A.fAxis,hybrid_coupler_A.antenna_gain_frequency.imag,color='k',ls='--')
#ax3.plot(hybrid_coupler_B.fAxis,hybrid_coupler_B.antenna_gain_frequency.real,color='grey')
#ax3.plot(hybrid_coupler_B.fAxis,hybrid_coupler_B.antenna_gain_frequency.imag,color='grey',ls='--')
#ax3.plot(cambridge_balun.fAxis,cambridge_balun.antenna_gain_frequency.real,color='r')
#ax3.plot(cambridge_balun.fAxis,cambridge_balun.antenna_gain_frequency.imag,color='r',ls='--')


fig1.savefig('Sinuous_s11_amp_comarision_August_29th_2017.pdf')
fig2.savefig('Sinuous_s11_pha_comarision_August_29th_2017.pdf')


plt.show()
