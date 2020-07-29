# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 13:40:00 2020

@author: GEUGYFH
"""
import scipy as sc
from scipy import signal
import pyqtgraph as pg
import numpy as np
import sys
import glob, os
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import mdfreader
import pandas as pd



pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)

base='D:/USUARIS/GEUGYFH\Desktop/LC1 Indian Project/Knocking Measure RON91 RON95/RON 95/Barrido'
files=os.listdir(base)

name_files=[]
for file in files:
    if file.endswith('.dat'):
        name_files.append(file)
        


info=mdfreader.MdfInfo()
Data_O=[]
Torque=[]
Speed=[]
Pedal=[]

# 'tans','psrrw','lamsoni_w','zwout','injmode_l_{0}','rlsol_w','rk_w','pcr_ntrbChMdl_VW','tmot','flamlu_w','wkrma','ora_w','fra_w','fr_w','wnwe_w','wnwa_w'
for i in range(0,len(name_files)):
# for i in range(0,1):
    ruta=base+'/'+name_files[i]
    channels=info.list_channels(ruta)
    channels.sort()
    Channel_list=['nmot_w','ActMod_trqInr','APP_r','tans','psrr_w','lamsoni_w','zwout','injmode_l_[0]','rlsol_w','rk_w','PCR_nTrbChMdl_VW','tmot','flamlu_w','wkrma','ora_w','fra_w','fr_w','wnwe_w','wnwa_w','PCR_rGov_VW','psrs_w','rl_w','TrbnByVlv_r','TrbnByVlv_rAct','ThrVlv_rAct','zwspae','tumg','wnwsa_w','wnwse_w','wdkba_w']
    Data=[]
    Time=[]
    Data_eval=[]
    for idlaod in range(0,len(Channel_list)):
        yop=mdfreader.Mdf(ruta, channel_list=[Channel_list[idlaod]], convert_after_read=True)
        Load_D=yop.get_channel(Channel_list[idlaod])
        Data.append(Load_D['data'])
        time_Name=yop.get_channel_master(Channel_list[idlaod])
        Load_T=yop.get_channel(time_Name)
        Time.append(Load_T['data'])
    
    Measure_T=np.max(Time[0])
    T_Lin=np.linspace(0.5, Measure_T-1,500)
    
    for idlaod_Conv in range(0,len(Channel_list)):
    
        Data_0_int=sc.interpolate.interp1d(Time[0],Data[0])
        Data_2_int=sc.interpolate.interp1d(Time[0],Data[2])
        Speed_interp=Data_0_int(T_Lin)
        Pedal_interp=Data_2_int(T_Lin)
        idx_init=np.where((Speed_interp>=np.min(Speed_interp)*1.05) & (Pedal_interp>=np.max(Pedal_interp)*0.98))
        idx_fin=np.where((Speed_interp>=np.max(Speed_interp)*0.98) & (Pedal_interp>=np.max(Pedal_interp)*0.98))
        
        Data_int=sc.interpolate.interp1d(Time[idlaod_Conv],Data[idlaod_Conv])
        
        Data_eval.append(Data_int(T_Lin)[idx_init[0][0]:idx_fin[0][0]])
   
    # Data_eval=np.stack(Data_eval)
    if i==0:
        Data_O=np.transpose(Data_eval)
    else:
        Data_O=np.concatenate((Data_O,np.transpose(Data_eval)))
    
    # Data_O.append(Data_eval)
    # Data_O=np.stack(np.stack(Data_O)) 
    
df = pd.DataFrame(Data_O)      
    ## save to xlsx file       
filepath = 'Export_Barrido_RON95Complete.xlsx'
    # with pd.ExcelWriter(filepath, engine="openpyxl",mode='a') as writer:  
    #     df.to_excel(writer)
df.to_excel(filepath, index=False)
    
#matplotlib inline
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
plt.style.use('seaborn-white')

for idxcol in range(0,len(Channel_list)-2):
    figure(num=None, figsize=(14, 8), dpi=120, facecolor='w', edgecolor='k')
 
       
    plt.title(Channel_list[idxcol+2])
    plt.xlabel('nmot_w [km/h]')
    plt.ylabel('ActMod_trqInr [Nm]')
    plt.xlim(1000, 6000)
    plt.grid()
    x = Data_O[:,0]
    y = Data_O[:,1]
    z = Data_O[:,idxcol+2]

    xi = np.linspace(np.min(x),np.max(x), 50)
    yi = np.linspace(np.min(y),np.max(y), 50)


    xi,yi = np.meshgrid(xi,yi)

    zi = griddata((x, y), z,(xi, yi),method='linear')

    contours = plt.contour(xi, yi, zi, 10, colors='k')


    plt.contourf(xi, yi, zi, 10, cmap='viridis')

    plt.clabel(contours,inline=True,fmt='%0.1f', colors='k', fontsize=10)

# plt.imshow(zi, extent=[0, 5, 0, 5], origin='lower',cmap='RdGy', alpha=0.5)
    plt.colorbar()
    
    plt.savefig(Channel_list[idxcol+2]+'RON95.png', bbox_inches='tight')








    
        
    # Speed.append(Speed_interp[idx_init[0][0]:idx_fin[0][0]])
    # Torque.append(Torque_interp[idx_init[0][0]:idx_fin[0][0]])
    # Pedal.append(Pedal_interp[idx_init[0][0]:idx_fin[0][0]])
    
    # Speed.append(Speed_interp)
    # Torque.append(Torque_interp)
    # Pedal.append(Pedal_interp)
    
    # Speed.append(Data_0_int(T_Lin))
    # Torque.append(Data_1_int(T_Lin))
    # Pedal.append(Data_2_int(T_Lin))
    
    
    # Data_G.append(Data)


# Salida=np.transpose([TUMG[0:-1],y_TMOT,TOEL_S[0:-1],y[0:-1]])
# df = pd.DataFrame (Salida)

# ## save to xlsx file

# filepath = 'Salida_10.xlsx'

# df.to_excel(filepath, index=False)


# win = pg.GraphicsWindow(title="Init")
# win.resize(1000,600)

# p5 = win.addPlot(title="Scatter plot")

# p5.plot(np.concatenate(Speed),np.concatenate(Torque),pen=None, symbol='o', symbolPen=None, symbolSize=6, symbolBrush=(100, 100, 255, 50))
# p5.plot(Time[0],Data[0])
# p5.plot(Time[1],Data[1],pen=pg.mkPen('b', width=2))
# p5.setLabel('left', "Y Axis", units='A')
# p5.setLabel('bottom', "Y Axis", units='s')
# p5.setLogMode(x=True, y=False)

        
# from pyqtgraph.Qt import QtCore, QtGui
# import pyqtgraph as pg
# import pyqtgraph.opengl as gl
# import numpy as np

# from scipy.interpolate import griddata

# ## Create a GL View widget to display data
# app = QtGui.QApplication([])
# w = gl.GLViewWidget()
# w.show()
# w.setWindowTitle('pyqtgraph example: GLSurfacePlot')
# w.setCameraPosition(distance=50)

# ## Add a grid to the view
# g = gl.GLGridItem()
# g.scale(2,2,1)
# g.setDepthValue(10)  # draw grid after surfaces since they may be translucent
# w.addItem(g)

# ## Saddle example with x and y specified
# x = np.linspace(-8, 8, 100)
        
# y = np.linspace(-8, 8, 100)
# z = 0.1 * ((x.reshape(100,1) ** 2) - (y.reshape(1,100) ** 2))


# xi,yi = np.meshgrid(np.concatenate(Speed),np.concatenate(Torque))
# zi = griddata((np.concatenate(Speed),np.concatenate(Torque)),np.concatenate(Pedal),(xi,yi),method='linear')


# p2 = gl.GLSurfacePlotItem(x=np.concatenate(Speed), y=np.concatenate(Torque), z=zi, shader='normalColor')
# # p2.translate(-10,-10,0)
        
# w.addItem(p2)
        
# if __name__ == '__main__':

#     if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#         QtGui.QApplication.instance().exec_()
        




# import pyqtgraph.examples as pyex
# pyex.run()

