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
parser.add_argument('--minamp','-m',type=float,default=-60,
                    help='maximum amplitude to plot')
parser.add_argument('--maxamp','-x',type=float,default=0,
                    help='minimum amplitude to plot')
#parser.add_argument('--zi','-z',type=float,default=None,help='ofiginal input impedance')
#parser.add_argument('--zo','-Z',type=float,default=None,help='new input impedance')

args=parser.parse_args()
configfile=args.input
fmin=args.fmin
fmax=args.fmax
domain=args.domain
ymin=args.minamp
ymax=args.maxamp
#zo=args.zo
#zi=args.zi
#if zo is None or zi is None:
#    changez=False
#else:
#    chanzez=True


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
linestyles=[]
changezs=[]
zis=[]
zfs=[]

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
        if line_items[10]=='' or line_items[10]=='\n':
            linestyles.append('-')
        else:
            linestyles.append(line_items[10])
        if len(line_items)==13:
            if line_items[11]=='True':
                changezs.append(True)
            else:
                changezs.append(False)
            zis.append(float(line_items[12]))
            zfs.append(floag(line_items[13]))
        else:
            changezs.append(False)
            zis.append(0.)
            zfs.append(0.)


fig1=plt.figure()
fig2=plt.figure()
ax1=fig1.add_axes([.1,.1,.8,.8])
ax2=fig2.add_axes([.1,.1,.8,.8])

for (prefix,postfix,
     filetype,meastype,
     label,color,lw,portmap,
     prefixb,postfixb,ls,changez,zi,zf) in zip(prefixes,postfixes,
                                               filetypes,meastypes,
                                               labels,colors,linewidths,portmaps,
                                               prefixesb,postfixesb,linestyles,changezs,zis,zfs):
    assert meastype in ['differential','balun','simulation','baluncal']
    if meastype=='simulation' or meastype=='baluncal':
        simulation=GD()
        simulation.read_files(prefix+postfix,filetype,fMin=fmin,fMax=fmax,changeZ=changez,z0=zi,z1=zf)
        if domain=='freq':
            db_s11=10.*np.log10(np.abs(simulation.gainFrequency))
            pha_s11=np.angle(simulation.gainFrequency)
            x=simulation.fAxis
        elif domain=='delay':
            db_s11=10.*np.log10(np.abs(simulation.gainDelay))
            pha_s11=np.angle(simulation.gainDelay)
            x=simulation.tAxis
            
    elif meastype=='balun':
        balunmeas=ABM()
        balunmeas.read_files(prefix,postfix,prefixb,postfixb,filetype,portmap[0],portmap[1],portmap[2],fMin=fmin,fMax=fmax,changeZ=changez,z0=zi,z1=zf)
        if domain=='freq':
            db_s11=10.*np.log10(np.abs(balunmeas.antenna_gain_frequency))
            db_s11_ucorr=10.*np.log10(np.abs(balunmeas.antenna_raw.gainFrequency))
            pha_s11=np.angle(balunmeas.antenna_gain_frequency)
            pha_s11_ucorr=np.angle(balunmeas.antenna_raw.gainFrequency)
            x=balunmeas.fAxis
        elif domain=='delay':
            db_s11=10.*np.log10(np.abs(balunmeas.antenna_gain_delay))
            db_s11_ucorr=10.*np.log10(np.abs(balunmeas.antenna_raw.gainDelay))
            pha_s11=np.angle(balunmeas.antenna_gain_delay)
            pha_s11_ucorr=np.angle(balunmeas.antenna_raw.gainDelay)
            x=balunmeas.tAxis
            
    elif meastype=='differential':
        no_balun=ADM()
        no_balun.read_files(prefix,postfix,filetype,fmin,fmax,changeZ=changez,z0=zi,z1=zf)
        if domain=='freq':
            db_s11=10.*np.log10(np.abs(no_balun.antenna_gain_frequency))
            pha_s11=np.angle(no_balun.antenna_gain_frequency)
            x=no_balun.fAxis
        elif domain=='delay':
            db_s11=10.*np.log10(np.abs(no_balun.antenna_gain_delay))
            pha_s11=np.angle(no_balun.antenna_gain_delay)
    ax1.plot(x,db_s11,linestyle=ls,color=color,lw=int(lw),label=label)
    ax2.plot(x,pha_s11,linestyle=ls,color=color,lw=int(lw),label=label)

ax1.grid()
fig1.set_size_inches(10,6)
if domain=='freq':
    ax1.set_xlabel('frequency (GHz)')
    ax1.set_ylabel('|S$_{11}$| (dB)')
    ax2.set_xlabel('frequency (GHz)')
    ax2.set_ylabel('Arg($S_{11}$) (rad)')
elif domain=='delay':
    ax1.set_xlabel('Delay (ns)')
    ax1.set_ylabel('$|\\widetilde{S}_{11}|$(dB)')
    ax2.set_xlabel('Delay (ns)')
    ax2.set_ylabel('Arg($\\widetilde{S}_{11}$) (rad)')
    ax1.set_xlim(-100,500)
    ax1.set_ylim(-50,0)
    ax2.set_xlim(-100,500)
ax1.set_ylim(ymin,ymax)
ax2.legend(loc='best')
ax1.legend(loc='best')
ax2.grid()
fig2.set_size_inches(10,6)


if args.output:
    fig2.savefig(args.output+'_pha.png',bbox_inches='tight')
    fig1.savefig(args.output+'_amp.png',bbox_inches='tight')


plt.show()
