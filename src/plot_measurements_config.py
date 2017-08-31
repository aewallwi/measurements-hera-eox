import numpy as np
from gainData import AntennaBalunMeasurement as ABM
from gainData import AntennaDiffMeasurement as ADM
from gainData import GainData as GD
import matplotlib.pyplot as plt
import sys
import argparse


parser=argparse.ArgumentParser(description='Plot S11 amplitude and phase for simulations and/or measurements using various techniques')
parser.add_argument('--input','-i',
                    dest='input',type=str,
                    help=('Name of config file with list of post(pre)fixes for files'
                          'and baluns.'))
parser.add_argument('--output','-o',
                    dest='output',type=str,
                    help=('Name of output plot file. default=None'
                          'If None, no plots saved.'),default=None)
parser.add_argument('--domain','-d',
                    dest='domain',type=str
                    help=('Domain of measurement.'),default='freq')
parser.add_argument('--min','-l',dest='fmin',type=float,
                    help=('minimum frequency'),default=0.05)
parser.add_argument('--max','-u',dest='fmax',type=float,
                    help=('maximum frequency'),default=0.25)

opts=parser.parse_args()
configfile=parser.input
fmin=parser.fmin
fmax=parser.fmax


prefixes=[]
postfixes=[]
prefixesb=[]
postfixesb=[]
colors=[]
labels=[]
colors=[]
filetypes=[]
linewidths=[]
meastypes=[]

configfile=sys.argv[0]

config_lines=open(configfile).read_lines
for line in config_lines:
    if '#' not in line:
        line_items=line.split(',')
        prefixes.append(line_items[0])
        postfixes.append(line_items[1])
        prefixesb.append(line_items[2])
        postfixesb.append(line_items[3])
        filetypes.append(line_items[4])
        meastypes.append(line_items[5])
        labels.append(line_items[6])
        colors.append(line_items[7])
        linewidths.append(line_items[8])




fig1=plt.figure()
fig2=plt.figure()
ax1=fig1.add_axes([.1,.1,.8,.8])
ax2=fig2.add_axes([.1,.1,.8,.8])


for (prefix,postfix,
     prefixb,postfixb,
     filetype,meastype,
     label,color,lw) in zip(prefixes,postfixes,
                            prefixesb,postfixesb,
                            filtetypes,meastypes,
                            labels,colors,linewidths):
    if meastype=='simulation':
        simulation=GD()
        simulation.read_files(prefix+postfix,filetype,fmin=fmin,fmax=fmax)
        simulation.read_files(prefix+postfix,filetype,fMin=fmax,fMax=fmin)
        simulation.gainFrequency=simulation.gainFrequency
        db_s11_sim=10.*np.log10(np.abs(simulation.gainFrequency))
        pha_s11_sim=np.angle(simulation.gainFrequency)
        ax1.plot(simulation.fAxis,db_s11_sim,color=color,lw=lw,label=label)
        ax2.plot(simulation.fAxis,pha_s11_sim,color=color,lw=lw,label=label)


for fnum,fname in enumerate(filenames):
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


ax1.grid()
fig1.set_size_inches(10,6)
ax1.set_xlabel('frequency (GHz)')
ax1.set_ylabel('|S$_{11}$| (dB)')
ax1.legend(loc='best')
ax2.grid()
fig2.set_size_inches(10,6)
ax2.set_xlabel('frequency (GHz)')
ax2.set_ylabel('Arg($S_{11}$) (rad)')
ax2.legend(loc='best')

fig1.savefig('Sinuous_s11_amp_comarision_August_30th_2017.pdf')
fig2.savefig('Sinuous_s11_pha_comarision_August_30th_2017.pdf')


plt.show()
