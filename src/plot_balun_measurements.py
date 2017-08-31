import numpy as np
from gainData import Balun
import gainData as GD
import matplotlib.pyplot as plt

#load measurements
hybrid_coupler_A=Balun()
hybrid_coupler_B=Balun()
hybrid_coupler_A_me=Balun()
cambridge_balun=Balun()


hybrid_coupler_A.read_files('../hybrid_coupler_A_Sierra/A_','','ANRITSU_CSV',
                            port1='1',port2='3',port3='4',fMin=0.05,fMax=0.25)
hybrid_coupler_A_me.read_files('../hybrid_coupler_A/hybrid_','','ANRITSU_CSV',
                            port1='1',port2='3',port3='4',fMin=0.05,fMax=0.25)
hybrid_coupler_B.read_files('../hybrid_coupler_B/1','','ANRITSU_CSV',
                            '1','3','4',0.05,0.25)
cambridge_balun.read_files('../Cambridge_Balun_Measurements_N/',
                           '','ANRITSU_CSV','1','2','3',fMin=0.05,fMax=0.25)


#load Jianshu's data


fig1=plt.figure()
fig2=plt.figure()
fig3=plt.figure()
fig4=plt.figure()

ax1=fig1.add_axes([.1,.1,.8,.8])
ax2=fig2.add_axes([.1,.1,.8,.8])
ax3=fig3.add_axes([.1,.1,.8,.8])
ax4=fig4.add_axes([.1,.1,.8,.8])

#angle_ratio=np.angle(hybrid_coupler_A_me.get_ss('s12'))-np.angle(hybrid_coupler_A_me.get_ss('s13'))
#angle_ratio=np.unwrap(angle_ratio)
#ax1.plot(angle_ratio)
#ax2.plot(np.real(hybrid_coupler_A_me.get_ss('s21')))
#ax2.plot(np.real(hybrid_coupler_A_me.get_ss('s31')))
#plt.show()



plotstrs=['s11','s1d','sd1','sdd','s1c','sc1','scc','scd','sdc']
#plotstrs=['s11','s12','s13','s21','s22','s23','s31','s32','s33']
#plotstrs=['s11']
for dstring in plotstrs:
    #print dstring
    y=np.abs(hybrid_coupler_A.get_ds(dstring))
    #print y
    y=10.*np.log10(y)
    x=hybrid_coupler_A.fAxis
    ax1.plot(x,y,label=dstring)
for dstring in plotstrs:
    #print dstring
    y=np.abs(hybrid_coupler_B.get_ds(dstring))
    #print y
    y=10.*np.log10(y)
    x=hybrid_coupler_B.fAxis
    ax2.plot(x,y,label=dstring)
for dstring in plotstrs:
    y=np.abs(hybrid_coupler_A_me.get_ds(dstring))
    y=10.*np.log10(y)
    x=hybrid_coupler_A_me.fAxis
    ax3.plot(x,y,label=dstring)
for dstring in plotstrs:
    print dstring
    y=np.abs(cambridge_balun.get_ds(dstring))
    y=10.*np.log10(y)
    print y
    x=cambridge_balun.fAxis
    ax4.plot(x,y,label=dstring)


ax2.legend(loc='best')
ax2.grid()
ax2.set_title('Hybrid Coupler B')
ax1.legend(loc='best')
ax1.grid()
ax1.set_title('Hybrid Coupler A')
ax3.legend(loc='best')
ax3.grid()
ax4.legend(loc='best')
ax4.grid()
ax4.set_title('Cambridge Balun')
ax1.set_ylim(-30,5)
ax2.set_ylim(-30,5)
ax3.set_ylim(-30,5)
ax4.set_ylim(-30,5)
fig1.savefig('hybrid_coupler_A.png')
fig2.savefig('hybrid_coupler_B.png')
fig4.savefig('cambridge_balun.png')
plt.show()

