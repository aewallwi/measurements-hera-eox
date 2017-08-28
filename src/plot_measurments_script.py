'''
Script for on-the-fly plotting of VNA data and comparison to simulation.
'''

import numpy as np
from gainData import AntennaBalunMeasurement as ABM
from gainData import AntennaDiffMeasurement as ADM
from gainData import GainData as GD
import matplotlib.pyplot as plt
import argparse
import os

#load measurements
hybrid_coupler_A=ABM()
hybrid_coupler_B=ABM()
cambridge_balun=ABM()
no_balun=ADM()


parser=argparse.ArgumentParser(description='Plot a VNA measurement versus simulation.')
parser.add_argument('--prefix','-b',
                    ,dest='prefix',type=str,help=('Name of the data file you wish to plot.'
                                                  'Should have format <prefix>smn<postfix>_amph/phase.txt'))
parser.add_argument('--postfix','-a',
                    ,dest='postfix',type=str,help=('postfix of the data file you wish to plot.'
                                                   'should have format <prefix>smn<postfix>_amp/phase.txt'))
parser.add_argument('--output','-o',
                    dest='outputfile',type=str,help='Name of output plot file.',default=None)
parser.add_argument('--sim','-s',
                    dest='simfile',type=str,help=('Name of Simulation file to compare.'
                                                  'If none, will not plot simulation'),default=None)
parser.add_argument('--balun','-b',
                    dest='balunfile',type=str,
                    help=('Name of the balun file.'
                          'Options must be A,B (for hybrid couplers A or B), C (for Cambridge),'
                          'or D (for a balun that has been calibrated out).'
                          'If none, script will assume no balun measurement'),default='N')
parser.add_argument('--performance','-u',dest='performance',type=bool,
                    default=False,help='Option to plot S11 spec in frequency')
parser.add_argument('--domain','-x',type=str,
                    help='Domain to plot S11 data in. Can be freq or delay',default='freq')

opts=parser.parse_args()

prefix=opts.prefix
postfix=opts.postfix
outputfile=opts.outputfile
simfile=opts.simfile
balun=opts.balun
performance=opts.performance
domain=opts.domain

#
#Assume that balun files are in the directory above this script.
#
balun_A_pref='../hybrid_coupler_A_Sierra/A_'
balun_B_pref='../hybrid_coupler_B/1'
cambridge_pref='../Cambridge_Balun_Measurements_N/'

assert domain in ['freq','delay']
measurements=[]
simulations=[]
if 'A' in balun:
    hc=ABM()
    hc.read_files(prefix,postfix,
                  '../hybrid_coupler_A_Sierra/A_','','ANRITSU_CSV',
                  '1','3','4',0.05,0.25)
    measurements.append(hc)
elif 'B' in balun:
    hc=ABM()
    hc.read_files(prefix,postfix,
                  '../hybrid_coupler_B/1','','ANRITSU_CSV',
                  '1','3','4',0.05,0.25)
    measurements.append(hc)
elif 'C' in balun:
    hc=ABM()
    hc.read_files(data,'_cambridge_balun_N_antenna_0','',
                  '../Cambridge_Balun_Measurements_N/','','ANRITSU_CSV',
                  '1','2','3',0.05,0.25)
    measurements.append(hc)
elif 'N' in balun:
    nb=ADM()
    nb.read_files(data,'ANRITSU_CSV',0.05,0.25)
    measurements.append(nb)
else:
    print('No valid balun option provided. Exiting...')
    exit()

if simfile:
    simulation=GD()
    simulation.read_files(simfile,'CST_S11',fMin=0.05,fMax=0.25)
    simulations.append(simulation)





    
#pha_s11_cam=np.angle(cambridge_balun.antenna_raw.gainFrequency)
#pha_s11_no_balun=np.angle(no_balun.antenna_gain_frequency)
#pha_s11_sim=np.angle(simulation.gainFrequency)

fig1=plt.figure()
fig2=plt.figure()

ax1=fig1.add_axes([.1,.1,.8,.8])
ax2=fig2.add_axes([.1,.1,.8,.8])


for meas in measurements:
    if domain=='freq':
        x=meas.fAxis
        y_a=10.*np.log10(np.abs(meas.antenna_gain_frequency))
        y_p=np.angle(meas.antenna_gain_frequency)
    elif domain=='delay':
        x=hc.tAxis
        y_a=10.*np.log10(np.abs(meas.antenna_gain_delay))
        y_p=np.angle(meas.antenna_gain_delay)

    
for sim in simulations:
    if domain=='freq':
        x=sim.fAxis
        y_a=10.*np.log10(np.abs(sim.gainFrequency))
        y_p=np.angle(sim.gainFrequency)
    elif domain=='delay':
        x=sim.tAxis
        y_a=10.*np.log10(np.abs(sim.gainDelay))
        y_p=np.angle(sim.gainDelay)
        ax1.plot(x,y_a,color='k',ls='-',alpha=1,label='simulation')
        ax2.plot(x,y_p,color='k',ls='-',alpha=1,label='simulation')
if domain=='delay':
    ax1.set_ylabel('|$\\tilde{S}_{11}$| (dB)')
    ax1.set_xlabel('delay (ns)')
    ax1.set_xlim(-100,300)
    ax1.set_ylim(-60,10)
    ax1.grid()
    ax2.set_xlabel('delay (ns)')
    ax2.set_ylabel('Arg($\\tilde{S}_{11}$) (rad)')
    ax2.set_xlim(-100,300)
    ax2.set_ylim(-2.*np.pi,2*np.pi)
if domain=='freq':          
    ax1.plot(x,y_a,color='r',ls='-',alpha=1,label='data')
    ax2.plot(x,y_p,color='r',ls='-',alpha=1,label='data')
    ax1.set_ylabel('|$S_{11}$| (dB)')
    ax1.set_xlabel('f (GHz)')
    ax1.set_xlim(0.05,0.25)
    ax1.set_ylim(-20,10)
    ax1.grid()
    ax2.set_xlabel('f (GHz)')
    ax2.set_ylabel('Arg($S_{11}$) (rad)')
    ax2.set_xlim(0.05,0.25)
    ax2.set_ylim(-2.*np.pi,2*np.pi)


if outputfile:
    fig1.savefig(outputfile+'_amp.pdf')
    fig2.savefig(outputfile+'_pha.pdf')

plt.show()
