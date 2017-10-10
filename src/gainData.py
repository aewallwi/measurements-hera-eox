#************************************************************
#library for reading cst and VNA data files
#************************************************************
import numpy as np
import healpy as hp
import numpy.fft as fft
import scipy.signal as signal
import matplotlib.pyplot as plt
import re as re
import scipy.interpolate as interp
import os
DEBUG=False
'''
A few transformation matrices for differential measurements
'''
TMAT3=np.sqrt(.5)*np.array([[1,0,0],[0,1,1],[0,1,-1]]).astype(complex)

#************************************************************
#transform a matrix
#************************************************************
def transform_matrix(matrix,tmatrix):
    return tmatrix.dot(matrix.dot(np.linalg.inv(tmatrix)))


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
    def __init__(self):
        self.device=''
        self.data=''
        self.comment=''
        self.datarange=''
    def set_info(self,device='',date='',dtype='',comment='',datarange=[]):
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
    meta=MetaData()
    meta.set_info(device=device,dtype=dtype,datarange=[FLOW,FHIGH,NDATA],comment=comment)
    return fAxis,data,meta

#read single Anritsu CSV File
def readAnritsuCSV(fname):
    funit=''
    if DEBUG:
        print('file='+fname)
    data=[]
    readData=False
    if '_pha' in fname:
        mode='PHASE'
    else:
        mode='AMP'
    for line in open(fname).readlines():
        if '#' in line:
            readData=False
        if DEBUG:
            print('readData='+str(readData))
        if readData:
            if DEBUG:
                print(line)
            lineSplit=line.split(',')
            try:
                datapoint=[float(lineSplit[0][1:-1]),float(lineSplit[1][1:-3])]
                if mode=='AMP':
                    datapoint[1]*=-1
                if DEBUG:
                    print('datapoint='+str(datapoint))
                data.append(datapoint)
            except ValueError:
                if DEBUG:
                    print('Using Master Tools Format.')
                    print('lineSplit='+str(lineSplit))
                candidates=([float(lineSplit[6]),float(lineSplit[7])])
                if DEBUG:
                    print('candidates='+str(candidates))
                    print(lineSplit[10]+'-'+lineSplit[11])
                if candidates[0]==0.:
                    if mode=='PHASE':
                        datapoint=float(lineSplit[11])
                    else:
                        datapoint=candidates[1]
                else:
                    if mode=='PHASE':
                        datapoint=float(lineSplit[9])
                    else:
                        datapoint=candidates[0]
                if DEBUG:
                    print(datapoint)
                data.append([float(lineSplit[5][:-4]),datapoint])
                #except:
                #    if DEBUG:
                #        print('invalid file')
        #if 'Frequency' in line and ('S11' in line or 'S21' in line):
        if 'Point,S11.Real,S11.Imag,S21.Real,S21.Imag,Frequency,RL/S11.Log.Mag,RL/S21.Log.Mag,S11.Mag,S11.Phase,S21.Mag,S21.Phase' in line:
            readData=True
        if '\"Frequency(MHz)\",\"Phase ' in line:
            readData=True
        if '\"Frequency(MHz)\",\"Log Mag ' in line:
            readData=True
        elif 'MHz' in line:
            funit=1e-3
        elif 'GHz' in line:
            funit=1
        elif 'Hz' in line:
            funit=1e-9
        elif 'kHz' in line:
            funit=1e-6
        
    if funit=='':
        funit=1e-3
        
    data=np.array(data)
    if DEBUG:
        print(data)
    if(np.mod(len(data),2)==1):
        data=data[:-1,:]
    data[:,0]*=funit
    return data

def readAnritsu(fname,comment=''):
    fname_amp=fname+'amp.csv'
    fname_pha=fname+'pha.csv'
    #check if pha exists. If not, look for phase instead
    if not os.path.exists(fname_amp):
        fname_amp=fname+'log.csv'
    #check if amp exists. If not, look for log instead
    if not os.path.exists(fname_pha):
        fname_pha=fname+'phase.csv'
    if not (os.path.exists(fname_pha) and os.path.exists(fname_amp)):
        raise ValueError(('Could not find phase %s '
                          'or amplitude %s')%(fname_amp,fname_pha))
    if DEBUG:
        print(fname_pha)
        print(fname_amp)
    data_amp=readAnritsuCSV(fname_amp)
    data_pha=readAnritsuCSV(fname_pha)
    freqs=data_pha[:,0]
    data=10**(data_amp[:,1]/20.)
    #this is a return loss measurement so if
    #the gain is positive there was almost
    #certainly a sign errors in reading
    #amplitudes and should be inverted. 
    #if np.abs(data).max()>=10.:
    #    data=1./data
    data=data*np.exp(1j*np.radians(data_pha[:,1]))
    meta=MetaData()
    meta.set_info(device='Anritsu 2024A VNA',dtype=['FREQ','GHz'],datarange=[freqs.min(),freqs.max(),len(freqs)],comment=comment)
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
    #print np.diff(freqs)
    #print freqs
    #plt.plot(np.diff(freqs))
    #plt.show()
    if(cstFlag):
        device='CST'
    else:
        device='DifferentialVNA'
    meta=MetaData()
    meta.set_info(device=device,dtype=['FREQ',fUnit],datarange=[freqs.min(),freqs.max(),len(freqs)],comment=comment)
    return freqs,data,meta
            
    

    

#Read HP VNA data used in Greenbank measurements
def readVNAHP(fileName,comment=''):
    dataFile=open(fileName)
    dataLines=dataFile.readlines()
    FLOW=1e-9*float(dataLines[6].split()[1]);FHIGH=1e-9*float(dataLines[6].split()[2]);
    NDATA=int(dataLines[6].split()[3])
    if 'END' in dataLines[-1]:
        data=np.genfromtxt(fileName,skip_header=9,skip_footer=1,delimiter=',')
    else:
        data=np.genfromtxt(fileName,skip_header=9,skip_footer=0,delimiter=',')
    device=dataLines[1][:-2]
    dtype=dataLines[4].split()[1]
    meta=MetaData()
    meta.set_info(device=device,dtype=['FREQ',dtype],datarange=[FLOW,FHIGH,NDATA],comment=comment)
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
        if('o1' in dataLines[lNum] or 'Port1' in dataLines[lNum]):
            thisTrace=outputTrace1
            lNum+=2
        elif('o2' in dataLines[lNum] or 'Port2' in dataLines[lNum]):
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
    print('len(inputtrace=%d'%(len(inputTrace)))
    print('len(outputtrace=%d'%(len(outputTrace1)))
    if(len(inputTrace)>0):
        inputTrace[:,0]*=tFactor
    if(len(outputTrace1)>0):
        outputTrace1[:,0]*=tFactor
    if(len(outputTrace2)>0):
        outputTrace2[:,0]*=tFactor
    if np.mod(len(inputTrace),2)==1:
        outputTrace1=outputTrace1[:-1,:]
        if len(outputTrace2)>0:
            outputTrace2=outputTrace2[:-1,:]
        if len(outputTrace1)>0:
            outputTrace1=outputTrace1[:-1,:]
        if len(inputTrace)>0:
            inputTrace=inputTrace[:-1,:]
        inputTrace=inputTrace[:-1,:]
    meta=MetaData()
    meta.set_info(device='CST',dtype=['TIME',dtype],datarange=[inputTrace[:,0].min(),inputTrace[:,0].max(),len(inputTrace[:,0])],comment=comment)
    return [inputTrace,outputTrace1,outputTrace2],meta

    
def readCSTS11(fileName,comment='',degrees=True):
    dB=False
    fname_abs=fileName+'_abs.txt'
    fname_pha=fileName+'_pha.txt'
    if not os.path.exists(fname_abs):
        fname_abs=fileName+'_amp.txt'
    #check if amp exists. If not, look for log instead
    if not os.path.exists(fname_pha):
        fname_pha=fileName+'_phase.txt'
    header=open(fname_abs).readlines()[:2]
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
    amp=np.loadtxt(fname_abs,skiprows=2)
    fAxis=amp[:,0]
    amp=amp[:,1]
    if(dB):
        amp=10.**(amp/20.)

    pha=np.loadtxt(fname_pha,skiprows=2)[:,1]
    if(degrees):
        pha*=np.pi/180.
    data=amp*np.exp(1j*pha)
    meta=MetaData()
    meta.set_info(device='CST',dtype=['FREQ','S11'],datarange=[fAxis.min(),fAxis.max(),len(fAxis)],comment=comment)
    return fFactor*fAxis,data,meta
    

FILETYPES=['CST_TimeTrace','CST_S11','VNAHP_S11','S11_CSV','S11_S1P','ANRITSU_CSV']
class GainData():
    def __init__(self):
        self.metaData=MetaData()
        
    def read_files(self,fileName,fileType,fMin=None,fMax=None,windowFunction=None,comment='',filterNegative=False,extrapolateBand=False,changeZ=False,z0=100,z1=100):
        assert fileType in FILETYPES
        if(windowFunction is None):
            windowFunction = 'blackman-harris'
        self.windowFunction=windowFunction
        if (fileType=='CST_TimeTrace'):
            [inputTrace,outputTrace,_],self.metaData=readCSTTimeTrace(fileName,comment=comment)
            if np.mod(len(inputTrace),2)==1:
                inputTrace=np.vstack([inputTrace[0,:],inputTrace])
                inputTrace[0,0]-=(inputTrace[2,0]-inputTrace[1,0])
                outputTrace=np.vstack([outputTrace[0,:],outputTrace])
                outputTrace[0,0]-=(outputTrace[2,0]-outputTrace[1,0])
            #plt.plot(inputTrace[:,0],inputTrace[:,1])
            #plt.plot(outputTrace[:,0],outputTrace[:,1])
            #plt.show()
            self.fAxis=fft.fftshift(fft.fftfreq(len(inputTrace)*2,inputTrace[1,0]-inputTrace[0,0]))
            self.gainFrequency=fftRatio(outputTrace[:,1],inputTrace[:,1])
            
        elif(fileType=='CST_S11'):
            self.fAxis,self.gainFrequency,self.metaData=readCSTS11(fileName,comment=comment)
        elif(fileType=='VNAHP_S11'):
            self.fAxis,self.gainFrequency,self.metaData=readVNAHP(fileName,comment=comment)
        elif(fileType=='S11_CSV'):
            self.fAxis,self.gainFrequency,self.metaData=readCSV(fileName,comment=comment)
        elif(fileType=='S11_S1P'):
            self.fAxis,self.gainFrequency,self.metaData=readS1P(fileName,comment=comment)
        elif(fileType=='ANRITSU_CSV'):
            self.fAxis,self.gainFrequency,self.metaData=readAnritsu(fileName,comment=comment)
        if(fMin is None):
            fMin=self.fAxis.min()            
        if(fMax is None):
            fMax=self.fAxis.max()
        if(extrapolateBand):
            if DEBUG:
                print(self.fAxis.min())
                print(self.fAxis.max())
            if(fMin<self.fAxis.min()):
                fitSelection=self.fAxis<self.fAxis.min()+.01
                pReal=np.polyfit(self.fAxis[fitSelection],np.real(self.gainFrequency[fitSelection]),1)
                pImag=np.polyfit(self.fAxis[fitSelection],np.imag(self.gainFrequency[fitSelection]),1)
                fLow=np.arange(self.fAxis.min(),fMin,self.fAxis[0]-self.fAxis[1])
                self.fAxis=np.hstack([fLow[::-1],self.fAxis])
                self.gainFrequency=np.hstack([pReal[0]*fLow[::-1]+pReal[1]+1j*(pImag[0]*fLow[::-1]+pImag[1]),self.gainFrequency])
                #plt.plot(self.fAxis[fitSelection],np.real(self.gainFrequency[fitSelection]),ls='none',marker='o')
                #plt.plot(self.fAxis[fitSelection],self.fAxis[fitSelection]*pReal[0]+pReal[1],ls='--',color='r')
                #plt.plot(fLow[::-1],fLow[::-1]*pReal[0]+pReal[1],color='k')
                #plt.show()
            if(fMax>self.fAxis.max()):
                fitSelection=self.fAxis>self.fAxis.max()-.01
                pReal=np.polyfit(self.fAxis[fitSelection],np.real(self.gainFrequency[fitSelection]),1)
                pImag=np.polyfit(self.fAxis[fitSelection],np.imag(self.gainFrequency[fitSelection]),1)
                fHigh=np.arange(self.fAxis.max(),fMax,self.fAxis[1]-self.fAxis[0])
                self.fAxis=np.hstack([self.fAxis,fHigh])
                self.gainFrequency=np.hstack([self.gainFrequency,pReal[0]*fHigh+pReal[1]+1j*(pImag[0]*fHigh+pImag[1])])

                    
        selection=np.logical_and(self.fAxis>=fMin,self.fAxis<=fMax)
        nf=len(np.where(selection)[0])
        if np.mod(nf,2)==1:
            nf+=1
            maxind=np.where(selection)[0].max()
            if maxind<len(selection)-1:
                selection[maxind+1]=True
            else:
                minind=np.where(selection)[0].min()
                if minind>0:
                    selection[minind-1]=True
                else:
                    nf-=2
                    selection[maxind]=False
        
                    
        self.fAxis=self.fAxis[selection]
        self.gainFrequency=self.gainFrequency[selection]
        if(windowFunction== 'blackman-harris'):
            wF=signal.blackmanharris(len(self.fAxis))
            wF/=np.sqrt(np.mean(wF**2.))
        else:
            wF=np.ones(len(self.fAxis))
        self.tAxis=fft.fftshift(fft.fftfreq(len(self.fAxis),self.fAxis[1]-self.fAxis[0]))
        if(filterNegative):
            gainDelay=fft.fftshift(fft.ifft(fft.fftshift(self.gainFrequency)))
            gainDelay[self.tAxis<0.]=0.
            self.gainFrequency=fft.fftshift(fft.fft(fft.fftshift(gainDelay)))
        self.gainDelay=fft.fftshift(fft.ifft(fft.fftshift(self.gainFrequency*wF)))
        if changeZ:
            self.change_impedance(z0,z1)
            

    def change_impedance(self,z0,z1):
        '''
        change the reference impedance.
        args:
        z0: original reference impedance
        z1: new reference impedance
        '''
        za=z0*(1+self.gainFrequency)/(1-self.gainFrequency)
        za=za.real+1j*za.imag
        self.gainFrequency=(za-z1)/(za+z1)
        wF=signal.blackmanharris(len(self.fAxis))
        wF/=np.sqrt(np.mean(wF**2.))
        self.gainDelay=fft.fftshift(fft.ifft(fft.fftshift(self.gainFrequency*wF)))
        
        
    def export_CST_freq_s11(self,outfile):
        '''
        export frequency S11 to a .txt file format output by CST
        '''
        spacer=''.join([' ' for m in range(21)])
        amp_str=('        Frequency / MHz                S1,1/abs,dB\n'
                 '----------------------------------------------------'
                 '------------------\n')
        pha_str=('        Frequency / MHz                S1,1/arg,degrees\n'
                 '---------------------------------------------------------'
                 '-------------\n')
        for freq,amp,pha in zip(self.fAxis,
                                np.abs(self.gainFrequency),
                                np.angle(self.gainFrequency)):
            amp_str+='%.8f'%(1e3*freq)+spacer+'%.8f\n'%(20.*np.log10(amp))
            pha_str+='%.8f'%(1e3*freq)+spacer+'%.8f\n'%(np.degrees(pha))
        f=open(outfile+'_amp.txt','w')
        f.write(amp_str)
        f.close()
        f=open(outfile+'_pha.txt','w')
        f.write(pha_str)
        f.close()
        
        
        
    def interpolate_subband(self,nfi,df,f0,full_output=False):
        '''
        interpolates a sub-band between fMin and fMax by 
        taking a windowed FFT at a bandwidth twice the
        requested bandwidth, extrapolating and interpolating 
        the delay-transform transform, and FT-ing back. 
        '''
        change_nfi=False
        fMin=f0-nfi/2*df
        if fMin < self.fAxis.min():
            fMin=self.fAxis.min()
            change_nfi=True
        fMax=f0+(nfi/2-1)*df
        if fMax > self.fAxis.max():
            fMax=self.fAxis.max()
            change_nfi=True
        if change_nfi:
            nfi=int(np.round(fMax/df-fMin/df))
            f0=fMin+nfi/2*df
        fAxis_interp=f0+np.arange(-nfi/2,nfi/2)*df
        tAxis_interp=fft.fftshift(fft.fftfreq(nfi,df))
        b=fMax-fMin
        select_max=np.min([self.fAxis.max(),f0+b])
        select_min=np.max([self.fAxis.min(),f0-b])
        selection=np.logical_and(self.fAxis>=select_min,self.fAxis<=select_max)
        nf=len(self.fAxis[selection])
        if np.mod(nf,2)==1:
            nf+=1
            maxind=np.where(selection)[0].max()
            if maxind < len(selection)-1:
                selection[maxind+1]=True
            else:
                minind=np.where(selection)[0].min()
                if minind > 0:
                    selection[minind-1]=True
                else:
                    nf-=2
                    selection[maxind]=False
                
                
        sub_band=self.gainFrequency[selection]
        sub_fAxis=self.fAxis[selection]
        window=signal.blackmanharris(nf)
        delay_band=fft.fftshift(fft.ifft(fft.fftshift(sub_band*window)))
        sub_tAxis=fft.fftshift(fft.fftfreq(len(sub_band),self.fAxis[1]-self.fAxis[0]))
        maxTime=sub_tAxis.max()
        minTimeExt=maxTime*1./3.
        maxTimeExt=maxTime*2./3.
        ext_select=np.logical_and(sub_tAxis<=maxTimeExt,sub_tAxis>=minTimeExt)
        ext_poly=np.polyfit(sub_tAxis[ext_select],np.log10(np.abs(delay_band[ext_select])),1)
        interp_func_abs=interp.interp1d(sub_tAxis,np.log10(np.abs(delay_band)))
        interp_func_arg=interp.interp1d(sub_tAxis,np.angle(delay_band))
        band_interp=np.zeros(nfi,dtype=complex)
        select_interp=np.logical_and(tAxis_interp>=0,tAxis_interp<maxTimeExt)
        band_interp[select_interp]=10**(interp_func_abs(tAxis_interp[select_interp]))*np.exp(1j*interp_func_arg(tAxis_interp[select_interp]))
        select_ext=tAxis_interp>=maxTimeExt
        band_interp[select_ext]=10**(tAxis_interp[select_ext]*ext_poly[0]+ext_poly[1])
        #band_interp[select_ext]=0.
        window_interp_func=interp.interp1d(sub_fAxis,signal.blackmanharris(len(sub_band)))
        wFactor=1./((fAxis_interp.max()-fAxis_interp.min())/(sub_fAxis.max()-sub_fAxis.min()))
        if DEBUG:
            print(wFactor)
        band_interp_f=fft.fftshift(fft.fft(fft.fftshift(band_interp)))*wFactor
        window_corr=window_interp_func(fAxis_interp)
        #band_interp_f/=window_corr
        if full_output:
            return sub_tAxis,delay_band,sub_fAxis,sub_band,tAxis_interp,band_interp,fAxis_interp,band_interp_f
        else:
            return fAxis_interp,band_interp_f
        
        
class Balun():
    '''
    This is an object designed to represent a balun measurement. It includes a list of nine single ended VNA measurements.
    '''
    def __init__(self):
        self.diff_port_dict={'1':0,'c':1,'d':2}
        self.port_dict={'1':0,'2':1,'3':2}
        self.s_matrix_list=[[GainData() for m in range(3)] for n in range(3)]

    def read_files(self,prefix,postfix,filetype,port1='1',port2='2',port3='3',fMin=0.05,fMax=0.250):
        '''
        initialize a balun object with a filename prefix, a postfix, and a filteype. This will create
        nine different gainData objects from files prefix_s<port1><port2>_postfix_amp/phase.(ext)
        where port A is the unbalanced input port of the balun and ports B/C are the balanced terminals
        Args:
        prefix, string, prefix filename 
        postfix, string postfix filename
        ext, extension of filename (e.g. '.txt, .csv')
        filteype, type of file (e.g. CST_S11)
        port1, string in s-matrix corresponding to unbalanced port
        port2, string in s-matrix corresponding to balanced terminal 1
        port3, string in s-matrix corresponding to balanced terminal 2
        '''
        self.portList=[port1,port2,port3]
        self.fMin=fMin
        self.fMax=fMax
        for m,astr in enumerate(self.portList):
            for n,bstr in enumerate(self.portList):
                fstr=(prefix+'s%s%s'+postfix)%(astr,bstr)
                if DEBUG:
                    print('file=%s'%fstr)
                self.s_matrix_list[m][n].read_files(fstr,filetype,fMin,fMax)
        if DEBUG:
            print(self.s_matrix_list)
        self.fAxis=self.s_matrix_list[0][0].fAxis
        self.nf=len(self.fAxis)
        self.df=self.fAxis[1]-self.fAxis[0]
        self.s_matrix_frequency=np.zeros((self.nf,3,3),dtype=complex)
        self.s_matrix_delay=np.zeros_like(self.s_matrix_frequency)
        self.s_matrix_frequency_diff=np.zeros_like(self.s_matrix_frequency)
        self.s_matrix_delay_diff=np.zeros_like(self.s_matrix_delay)
        for chan in range(self.nf):
            for ind_a in range(3):
                for ind_b in range(3):
                    self.s_matrix_frequency[chan,ind_a,ind_b]=self.s_matrix_list[ind_a][ind_b].gainFrequency[chan]
                    self.s_matrix_delay[chan,ind_a,ind_b]=self.s_matrix_list[ind_a][ind_b].gainDelay[chan]
            self.s_matrix_frequency_diff[chan]=transform_matrix(self.s_matrix_frequency[chan].squeeze(),TMAT3)
            self.s_matrix_delay_diff[chan]=transform_matrix(self.s_matrix_delay[chan].squeeze(),TMAT3)
            if DEBUG:
                print(self.s_matrix_frequency[chan])
            
    def get_ds(self,idstr,domain='frequency',chans=None):
        if chans is None:
            chan_select=[m for m in range(self.nf)]
        porta=self.diff_port_dict[idstr[1]]
        portb=self.diff_port_dict[idstr[2]]
        if domain=='frequency':
            return self.s_matrix_frequency_diff[chan_select,porta,portb]
        else:
            return self.s_matrix_delay_diff[chan_select,porta,portb]

    def get_ss(self,idstr,domain='frequency',chans=None):
        if chans is None:
            chan_select=[m for m in range(self.nf)]
        porta=self.port_dict[idstr[1]]
        portb=self.port_dict[idstr[2]]
        if domain=='frequency':
            return self.s_matrix_frequency[chan_select,porta,portb]
        else:
            return self.s_matrix_delay[chan_select,porta,portb]
        
            
class AntennaBalunMeasurement():
    '''
    Object representing a measurement of antenna s-matrix using a balun. 
    Contains a balun object along with a single gain data object to 
    represent the raw antenna measurement and another gain data object 
    to represent the balun corrected antenna measurement. 
    '''
    def __init__(self):
        self.balun=Balun()
        self.antenna_raw=GainData()
    def read_files(self,ant_prefix,ant_postfix,
                   balun_prefix,balun_postfix,filetype,
                   port1_balun,port2_balun,port3_balun,fMin=0.05,fMax=0.25,
                   changeZ=False,z0=100.,z1=100.):
        self.balun.read_files(balun_prefix,balun_postfix,filetype,
                              port1_balun,port2_balun,port3_balun,fMin,fMax)
        self.antenna_raw.read_files(ant_prefix+'s11'+ant_postfix,
                                    filetype,fMin,fMax,)
        self.fAxis=self.antenna_raw.fAxis
        self.tAxis=self.antenna_raw.tAxis
        self.antenna_gain_frequency=np.zeros_like(self.antenna_raw.gainFrequency)
        self.antenna_gain_delay=np.zeros_like(self.antenna_raw.gainFrequency)
        self.nf=self.fAxis.shape[0]
        measdiff_f=self.antenna_raw.gainFrequency-self.balun.get_ds('s11')
        measdiff_t=self.antenna_raw.gainDelay-self.balun.get_ds('s11',domain='delay')
        self.antenna_gain_frequency=measdiff_f/\
                                     (self.balun.get_ds('s1d')*self.balun.get_ds('sd1')+\
                                      self.balun.get_ds('sdd')*measdiff_f)
        if changeZ:
            za=z0*(1+self.antenna_gain_frequency)/(1-self.antenna_gain_frequency)
            self.antenna_gain_frequency=(za-z1)/(za+z1)
        self.antenna_gain_delay=fft.fftshift(fft.ifft(fft.fftshift(self.antenna_gain_frequency)))
    
class AntennaDiffMeasurement():
    '''
    object represents measurement of differential antenna parameters with no balun. 
    '''
    def __init__(self):
        self.unbalanced_list=[[GainData() for m in range(2)] for n in range(2)]
    def read_files(self,ant_prefix,ant_postfix,filetype,fMin=0.05,fMax=0.25,changeZ=False,z0=100.,z1=100.):
        for a,astr in enumerate(['1','2']):
            for b,bstr in enumerate(['1','2']):
                self.unbalanced_list[a][b].read_files(ant_prefix+'s%s%s'%(astr,bstr)+ant_postfix,
                                                      filetype,fMin,fMax,changeZ=changeZ,z0=z0,z1=z1)
        self.fAxis=self.unbalanced_list[0][0].fAxis
        self.tAxis=self.unbalanced_list[0][0].tAxis
        self.antenna_gain_frequency=np.zeros_like(self.unbalanced_list[0][0].gainFrequency)
        self.antenna_gain_delay=np.zeros_like(self.unbalanced_list[0][0].gainFrequency)
        self.nf=self.fAxis.shape[0]
        for chan in range(self.nf):
            self.antenna_gain_frequency[chan]=.5*(self.unbalanced_list[0][0].gainFrequency[chan]+self.unbalanced_list[1][1].gainFrequency[chan]\
                                                  -self.unbalanced_list[1][0].gainFrequency[chan]-self.unbalanced_list[0][1].gainFrequency[chan])
            self.antenna_gain_delay[chan]=0.5*(self.unbalanced_list[0][0].gainDelay[chan]+self.unbalanced_list[1][1].gainDelay[chan]\
                                               -self.unbalanced_list[1][0].gainDelay[chan]-self.unbalanced_list[0][1].gainDelay[chan])



