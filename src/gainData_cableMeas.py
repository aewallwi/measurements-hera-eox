DEBUG=False
#************************************************************
#library for reading cst and VNA data files
#************************************************************
import numpy as np
import healpy as hp
import numpy.fft as fft
import scipy.signal as signal
import matplotlib.pyplot as plt
import re as re


#************************************************************
#compute delay spectrum in the same way that Nicolas does
#************************************************************
def ftUK(times,data):
    '''
    -import these data, resample them at a constant rate and do an extrapolation up to 0 MHz
    -do an IFFT (with zero padding) of the frequency signals, and take 20*log10(|S11|) to convert it in dB
    -plot the envelop of this time signal
    -so in these plots, to make it simple I did not apply a specific windowing function, it is just a "square" from 0 to 250 MHz, but this can be modified
    '''
    return None



class MetaData():
    def __init__(self,device='',date='',dtype='',comment='',datarange=[]):
        self.device=device
        self.date=date
        self.dtype=dtype
        self.comment=comment 
        self.datarange=datarange

#read csv file
def readCSV(fileName,comment='',device='',dtype=['','']):
    #data=n.loadtxt(fileName,delimiter=',',skiprows=1,dtype=n.complex)
    file=open(fileName)
    lines=file.readlines()
    lines=lines[0].split('\r')
    header=lines[0]
    lines=lines[1:]
    fAxis=[]
    data=[]
    for line in lines:
        tokens=line.split(',')
        fAxis.append(float(tokens[0]))
        tokens=tokens[1].split(' ')
        data.append(float(tokens[0])+float(tokens[1]+'1')*1j*float(tokens[2][:-1]))
    fAxis=n.array(fAxis)
    data=n.array(data)
    NDATA=len(data)
    fAxis*=1e-9
    FLOW=fAxis[0]
    FHIGH=fAxis[-1]
    meta=MetaData(device=device,dtype=dtype,datarange=[FLOW,FHIGH,NDATA],comment=comment)
    return fAxis,data,meta

#read single Anritsu CSV File
def readAnritsuCSV(fname):
    if DEBUG:
        print(fname)
    data=[]
    readData=False
    if 'pha' in fname:
        mode='PHASE'
    else:
        mode='AMP'
    for line in open(fname).readlines():
        if DEBUG:
            print('readData='+str(readData))
        if readData:
            if DEBUG:
                print(line)
            lineSplit=line.split(',')
            try:
                data.append([float(lineSplit[0][1:-1]),float(lineSplit[1][1:-3])])
            except:
                try:
                    candidates=([float(lineSplit[6]),float(lineSplit[7])])
                    if DEBUG:
                        print(candidates)
                        print(lineSplit[10]+'-'+lineSplit[11])
                    if candidates[0]==0.:
                        if mode=='PHASE':
                            datapoint=float(lineSplit[11])
                        else:
                            datapoint=-candidates[1]
                    else:
                        if mode=='PHASE':
                            datapoint=float(lineSplit[10])
                        else:
                            datapoint=-candidates[0]
                    if DEBUG:
                        print datapoint
                    data.append([float(lineSplit[5][:-4]),datapoint])
                except:
                    if DEBUG:
                        print('invalid file')
        if 'Frequency' in line and ('S11' in line or 'S21' in line):
            readData=True
        if 'MHz' in line:
            funit=1e-3
    data=np.array(data)
    if DEBUG:
        print(data)
    if(np.mod(len(data),2)==1):
        data=data[:-1,:]
    data[:,0]*=funit
    return data

def readAnritsu(fname,comment=''):
    fname_amp=fname+'_amp.csv'
    fname_pha=fname+'_pha.csv'
    data_amp=readAnritsuCSV(fname_amp)
    data_pha=readAnritsuCSV(fname_pha)
    freqs=data_pha[:,0]
    data=10**(-data_amp[:,1]/20.)
    #this is a return loss measurement so if
    #the gain is positive there was almost
    #certainly a sign errors in reading
    #amplitudes and should be inverted. 
    if np.abs(data).max()>=10.:
        data=1./data
    data=data*np.exp(1j*np.radians(data_pha[:,1]))
    meta=MetaData(device='Anritsu 2024A VNA',dtype=['FREQ','GHz'],datarange=[freqs.min(),freqs.max(),len(freqs)],comment=comment)
    return freqs,data,meta

#Read S-parameter file supplied by Nicolas
def readS1P(fileName,mode='simu',comment=''):
    fileLines=open(fileName).readlines()
    cstFlag=False
    data=[]
    freqs=[]
    for line in fileLines:
        if 'CST' in line:
            cstFlag=True
        if line[0]=='#':
            if 'MHz' in line or 'MHZ' in line:
                mFactor=1e-3
                fUnit='MHz'
            elif 'GHz' in line or 'GHZ' in line:
                mFactor=1
                fUnit='GHz'
            elif 'Hz' in line or 'HZ' in line:
                mFactor=1e-9
                fUnit='Hz'
            elif 'kHz' in line or 'KHZ' in line:
                mFactor=1e-6
                fUnit='kHz'
        if not(line[0]=='!' or line[0] =='#'):
            splitLine=line.split()
            freqs.append(float(splitLine[0]))
            data.append(float(splitLine[1])*np.exp(1j*np.radians(float(splitLine[2]))))
    data=np.array(data)
    freqs=np.array(freqs)*mFactor
    print np.diff(freqs)
    print freqs
    plt.plot(np.diff(freqs))
    plt.show()
    if(cstFlag):
        device='CST'
    else:
        device='DifferentialVNA'
    meta=MetaData(device=device,dtype=['FREQ',fUnit],datarange=[freqs.min(),freqs.max(),len(freqs)],comment=comment)
    return freqs,data,meta
            
    

    

#Read HP VNA data used in Greenbank measurements
def readVNAHP(fileName,comment=''):
    dataFile=open(fileName)
    dataLines=dataFile.readlines()
    FLOW=1e-9*float(dataLines[6].split()[1]);FHIGH=1e-9*float(dataLines[6].split()[2]);
    NDATA=int(dataLines[6].split()[3])
    data=np.loadtxt(fileName,skiprows=9,delimiter=',')
    device=dataLines[1][:-2]
    dtype=dataLines[4].split()[1]
    meta=MetaData(device=device,dtype=['FREQ',dtype],datarange=[FLOW,FHIGH,NDATA],comment=comment)
    fAxis=np.arange(NDATA)*(FHIGH-FLOW)/NDATA+FLOW
    return fAxis,data[:,0]+1j*data[:,1],meta

#take ratio of fft of two inputs with padding
def fftRatio(convolved,kernel):
    nf=len(convolved)
    convolved_pad=np.pad(convolved,(nf/2,nf/2),mode='constant')
    kernel_pad=np.pad(kernel,(nf/2,nf/2),mode='constant')
    return fft.fftshift(fft.fft(convolved_pad)/fft.fft(kernel_pad))
    

#Read CST time trace file
def readCSTTimeTrace(fileName,comment=''):
    dataFile=open(fileName)
    dataLines=dataFile.readlines()
    header=dataLines[:2]
    if('ns' in header[0]):
        tFactor=1.
    if('ms' in header[0]):
        tFactor=1e6
    if('micro' in header[0]):
        tFactor=1e3
    if('sec' in header[0]):
        tFactor=1e9
    inputTrace=[]
    outputTrace1=[]
    outputTrace2=[]
    lNum=0
    while lNum <len(dataLines):
        if('o1' in dataLines[lNum]):
            thisTrace=outputTrace1
            lNum+=2
        elif('o2' in dataLines[lNum]):
            thisTrace=outputTrace2
            lNum+=2
        elif('i1' in dataLines[lNum]):
            thisTrace=inputTrace
            lNum+=2
            dtype='Terminal Excitation'
        elif('Plane wave' in dataLines[lNum]):
            thisTrace=inputTrace
            lNum+=2
            dtype='PlaneWave Excitation'
        else:
            entry=dataLines[lNum].split()
            if(len(entry)==2):
                thisTrace.append([float(entry[0]),float(entry[1])])
            lNum+=1
    inputTrace=np.array(inputTrace)
    outputTrace1=np.array(outputTrace1)
    outputTrace2=np.array(outputTrace2)
    inputTrace[:,0]*=tFactor
    outputTrace1[:,0]*=tFactor
    if(len(outputTrace2)>0):
        outputTrace2[:,0]*=tFactor
    meta=MetaData(device='CST',dtype=['TIME',dtype],datarange=[inputTrace[:,0].min(),inputTrace[:,0].max(),len(inputTrace[:,0])],comment=comment)
    return [inputTrace,outputTrace1,outputTrace2],meta
    
def readCSTS11(fileName,comment='',degrees=True):
    dB=False
    header=open(fileName+'_abs.txt').readlines()[:2]
    if('MHz' in header[0]):
        fFactor=1e-3
    elif('GHz' in header[0]):
        fFactor=1e0
    elif('kHz' in header[0]):
        fFactor=1e-6
    elif('Hz' in header[0]):
        fFactor=1e-9
    if('dB' in header[0]):
        dB=True
    amp=np.loadtxt(fileName+'_abs.txt',skiprows=2)
    fAxis=amp[:,0]
    amp=amp[:,1]
    if(dB):
        amp=10.**(amp/20.)

    pha=np.loadtxt(fileName+'_pha.txt',skiprows=2)[:,1]
    if(degrees):
        pha*=np.pi/180.
    data=amp*np.exp(1j*pha)
    meta=MetaData(device='CST',dtype=['FREQ','S11'],datarange=[fAxis.min(),fAxis.max(),len(fAxis)],comment=comment)
    return fFactor*fAxis,data,meta
    

FILETYPES=['CST_TimeTrace','CST_S11','VNAHP_S11','S11_CSV','S11_S1P','ANRITSU_CSV']
FILETYPESDIFF=['ANRITSU_CSV']
class GainData():
    def __init__(self,fileName,fileType,fMin=None,fMax=None,windowFunction=None,comment='',filterNegative=False):
        assert fileType in FILETYPES
        if(windowFunction is None):
            windowFunction = 'blackman-harris'
        self.windowFunction=windowFunction
        if (fileType=='CST_TimeTrace'):
            [inputTrace,outputTrace,_],self.metaData=readCSTTimeTrace(fileName,comment=comment)
            self.fAxis=fft.fftshift(fft.fftfreq(len(inputTrace)*2,inputTrace[1,0]-inputTrace[0,0]))
            self.gainFrequency=fftRatio(outputTrace[:,1],inputTrace[:,1])
            
        elif(fileType=='CST_S11'):
            self.fAxis,self.gainFrequency,self.metaData=readCSTS11(fileName,comment=comment)
        elif(fileType=='VNAHP_S11'):
            self.fAxis,self.gainFrequency,self.metaData=readVNAHP(fileName,comment=comment)
        elif(fileType=='S11_CSV'):
            self.fAxis,self.gainFrequency,self.metaData=readCSV(fileName,comment=comment)
        elif(fileType=='ANRITSU_CSV'):
            self.fAxis,self.gainFrequency,self.metaData=readAnritsu(fileName,comment=comment)
        elif(fileType=='S11_S1P'):
            self.fAxis,self.gainFrequency,self.metaData=readS1P(fileName,comment=comment)
        if(fMin is None):
            fMin=self.fAxis.min()            
        if(fMax is None):
            fMax=self.fAxis.max()
        
        selection=np.logical_and(self.fAxis>=fMin,self.fAxis<=fMax)
        self.fAxis=self.fAxis[selection]
        self.gainFrequency=self.gainFrequency[selection]
        if(windowFunction== 'blackman-harris'):
            wF=signal.blackmanharris(len(self.fAxis))
            wF/=np.sqrt(np.mean(wF**2.))
        elif(windowFunction=='tophat'):
            wF=np.ones_like(self.fAxis)
        else:
            wF=np.ones(len(self.fAxis))
        self.tAxis=fft.fftshift(fft.fftfreq(len(self.fAxis),self.fAxis[1]-self.fAxis[0]))
        if(filterNegative):
            gainDelay=fft.fftshift(fft.ifft(fft.fftshift(self.gainFrequency)))
            gainDelay[self.tAxis<0.]=0.
            self.gainFrequency=fft.fftshift(fft.fft(fft.fftshift(gainDelay)))
        self.gainDelay=fft.fftshift(fft.ifft(fft.fftshift(self.gainFrequency*wF)))
class GainDataDiff():
    """
    Class representing a single differential measurement or simulation
    """
    def __init__(self,fileList,fileType,fMin=None,fMax=None,windowFunction=None,comment='',filterNegative=False):
        """
        fileList contains files for S11 S21 S12 S22
        """
        assert fileType in FILETYPESDIFF
        if windowFunction is None:
            windowFunction='blackman-harris'
        self.windowFunction=windowFunction


        self.S11=GainData(fileList[0],fileType,
                          fMin,fMax,windowFunction,
                          comment,filterNegative)
        self.S21=GainData(fileList[1],fileType,
                          fMin,fMax,windowFunction,
                          comment,filterNegative)
        self.S12=GainData(fileList[2],fileType,
                          fMin,fMax,windowFunction,
                          comment,filterNegative)
        self.S22=GainData(fileList[3],fileType,
                          fMin,fMax,windowFunction,
                          comment,filterNegative)
        #now set up frequency and time quantities
        self.fAxis=self.S11.fAxis
        self.tAxis=self.S11.tAxis
        self.gainFrequency=(self.S11.gainFrequency+\
                            self.S22.gainFrequency-\
                            self.S21.gainFrequency-\
                            self.S12.gainFrequency)/2.
        self.gainDelay=(self.S11.gainDelay+\
                        self.S22.gainDelay-\
                        self.S21.gainDelay-\
                        self.S12.gainDelay)/2.
        
