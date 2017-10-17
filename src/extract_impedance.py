import numpy as np
import gainData as gd
import argparse
parser=argparse.ArgumentParser(description='Extract antenna impedance')

parser.add_argument('--snot','-s',dest='snot',dtype=str)
parser.add_argument('--znot','-z',dest='znot',dtype=str)
parser.add_argument('--isant','-a',dest='isant',dtype=str,
                    help=('if "True", will assume that the provided z0'
                          'is the antenna impedance and will retrieve
                          termination'))
parser.add_argument('--ftype','-f',dest='filetype',dtype=str,
                    help=('type of file in S11'))
parser.add_argument('--fmin','-l',dest='fmin',dtype=float,
                    help=('lower frequency in GHz'))
parser.add_argument('--fmax','-u',dest='fmax',dtype=float,
                    help=('upper frequency in GHz'))
parser.add_argument('--output','-o',dest='output',dtype=strk
                    help=('name of output file'))

args=parser.parse_args()
znot=parser.znot
snot=parser.snot
isant=parser.isant
ftype=parser.filetype
if isant=="True":
    isant=True
else:
    isant=False
if not("s1p" in znot or 'z1p' in znot or "txt" in znot):
    znot=float(znot)
g=gd.GainData()
g.read_files(snot,ftype,args.flow,args.fmax)
zout=g.get_impedance(znot,isant=isant)
fout=g.fAxis()
f=open(args.output,'wb')
f.write(('! Touchstone file spoofed by extract_impedance.py \n'
         '! Z11=%s \n'
         '! S11=%s \n'
         '! Tree Item\n'
         '# MHZ Z RI R 1 \n'))%(znot,snot)
for chan in range(len(fout.shape[0])):
    f.write('%.5f\t%.5f\t%.5f\n'%(fout[chan],zout[chan].real,zout[chan].imag))
f.close()

