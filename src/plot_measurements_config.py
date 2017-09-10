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
                    type=str,
                    help=('Name of output plot file. default=None'
                          'If None, no plots saved.'),default=None)
parser.add_argument('--domain','-d',
                    type=str,
                    help=('Domain of measurement.'),default='freq')
parser.add_argument('--fmin','-l',type=float,
                    help=('minimum frequency'),default=0.05)
parser.add_argument('--fmax','-u',type=float,
                    help=('maximum frequency'),default=0.25)

args=parser.parse_args()
configfile=args.input
fmin=args.fmin
fmax=args.fmax



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
portmaps=[]

config_lines=open(configfile).readlines()
for line in config_lines:
    if '#' not in line:
        line_items=line.split(',')
        prefixes.append(line_items[0])
        postfixes.append(line_items[1])
        filetypes.append(line_items[2])
        meastypes.append(line_items[3])
        labels.append(line_items[4])
        colors.append(line_items[5])
        linewidths.append(line_items[6])
        prefixesb.append(line_items[7])
        postfixesb.append(line_items[8])
        portmaps.append(line_items[9])




fig1=plt.figure()
fig2=plt.figure()
ax1=fig1.add_axes([.1,.1,.8,.8])
ax2=fig2.add_axes([.1,.1,.8,.8])


for (prefix,postfix,
     filetype,meastype,
     label,color,lw,portmap,
     prefixb,postfixb) in zip(prefixes,postfixes,
                              filetypes,meastypes,
                              labels,colors,linewidths,portmaps,
                              prefixesb,postfixesb):
    assert meastype in ['differential','balun','simulation','baluncal']
    if meastype=='simulation' or meastype=='baluncal':
        simulation=GD()
        simulation.read_files(prefix+postfix,filetype,fMin=fmin,fMax=fmax)
        simulation.gainFrequency=simulation.gainFrequency
        db_s11=10.*np.log10(np.abs(simulation.gainFrequency))
        pha_s11=np.angle(simulation.gainFrequency)
        freqs=simulation.fAxis
    elif meastype=='balun':
        balunmeas=ABM()
        balunmeas.read_files(prefix,postfix,prefixb,postfixb,filetype,portmap[0],portmap[1],portmap[2])
        db_s11=10.*np.log10(np.abs(balunmeas.antenna_gain_frequency))
        db_s11_ucorr=10.*np.log10(np.abs(balunmeas.antenna_raw.gainFrequency))
        pha_s11=np.angle(balunmeas.antenna_gain_frequency)
        pha_s11_ucorr=np.angle(balunmeas.antenna_raw.gainFrequency)
        freqs=balunmeas.fAxis
    elif meastype=='differential':
        no_balun=ADM()
        no_balun.read_files(prefix,postfix,filetype,fmin,fmax)
        db_s11=10.*np.log10(np.abs(no_balun.antenna_gain_frequency))
        pha_s11=np.angle(no_balun.antenna_gain_frequency)
        freqs=no_balun.fAxis
    ax1.plot(freqs,db_s11,color=color,lw=lw,label=label)
    ax2.plot(freqs,pha_s11,color=color,lw=lw,label=label)

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

if args.output:
    fig2.savefig(args.output+'_pha.png',bbox_inches='tight')
    fig1.savefig(args.output+'_amp.png',bbox_inches='tight')


plt.show()
