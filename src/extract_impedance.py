import numpy as np
import gainData as gd
import argparse
parser=argparse.ArgumentParser(description='Extract antenna impedance')

parser.add_argument('--snot','-s',dest='snot')
parser.add_argument('--znot','-z',dest='znot')
parser.add_argument('--isant','-a',dest='isant',
                    help=('if "True", will assume that the provided z0'
                          'is the antenna impedance and will retrieve'
                          'termination'))
parser.add_argument('--ftype','-f',dest='filetype',
                    help=('type of file in S11'))
parser.add_argument('--fmin','-l',dest='fmin',
                    help=('lower frequency in GHz'))
parser.add_argument('--fmax','-u',dest='fmax',
                    help=('upper frequency in GHz'))
parser.add_argument('--output','-o',dest='output',
                    help=('name of output file'))

args=parser.parse_args()
znot=args.znot
snot=args.snot
isant=args.isant
ftype=args.filetype
if isant=="True":
    isant=True
else:
    isant=False
if not("s1p" in znot or 'z1p' in znot or "txt" in znot):
    znot=float(znot)
g=gd.GainData()
g.read_files(snot,ftype,float(args.fmin),float(args.fmax))
zout=g.get_impedance(znot,isant=isant)
fout=g.fAxis
f=open(args.output,'wb')
f.write(('! Touchstone file spoofed by extract_impedance.py \n'
         '! Z11=%s \n'
         '! S11=%s \n'
         '! Tree Item\n'
         '# MHZ Z RI R 1 \n')%(znot,snot))
for chan in range(fout.shape[0]):
    f.write('%.5f\t%.5f\t%.5f\n'%(fout[chan],zout[chan].real,zout[chan].imag))
f.close()

