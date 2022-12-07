import os
import pandas as pd
import numpy as np

import scipy as sp
from scipy import signal

import matplotlib.pyplot as plt


path = "./training_data"
gestures = {0:"rest",
            1:"剪刀",
            2:"石頭",
            3:"布",
            4:"手腕:上",
            5:"手腕:下",
            6:"手腕:內",
            7:"手腕:外",
            8:"OK",
            9:"大拇指"}


def emg_filter(data):
    emg = data[:,2:6]
    fsr = data[:,0:2]
    
    m = np.mean(emg,  axis = 0)
    pemg = emg - m

    
    l=1000
    
    high = 2*55/l
    low = 2*65/l
    b, a = signal.butter(4, [high,low], btype='bandstop')
    
    pemg = signal.filtfilt(b, a, pemg, axis=0)
    
    high = 2*10/l
    low = 2*450/l
    b, a = signal.butter(4, [high,low], btype='bandpass')
    
    pemg = signal.filtfilt(b, a, pemg, axis=0)
    
    pdata = np.concatenate([fsr, pemg], axis=1)
    
    return pdata

while True:

    print(gestures)

    gesture=input("手勢編號 :") 
    
    if (gesture.isdigit() == False):
        print("not a number")
        continue
    
    fig = plt.figure()
    plt.plot(np.zeros((6,2000)))
    fig.set_size_inches(w=19,h=7)
    plt.show()
    
    path_dir = os.path.join(path, gesture) # 路徑 + 手勢編號
    
    
    if os.path.isdir(path_dir): # 如果這個檔案是資料夾
        fds=os.listdir(path_dir) # 手勢編號下的所有檔案
        
        for j in range(len(fds)):  # 相同手勢編號下的每個檔案
            csv = fds[j] # 獲得csv檔名
            path_csv = os.path.join(path_dir, csv) #csv檔路徑
            df = pd.read_csv( path_csv)#讀取csv檔

            #X_data.append
            df1 = df.head(2000) #從這個class開始第一筆資料後面取2000
                
            #DataFrame to numpy
            df2 = df1.to_numpy() #DataFrame轉成Numpy array
            
            #EMG filter
            EMG = emg_filter(df2)

            fig = plt.figure()
            plt.plot(EMG)
            fig.set_size_inches(w=19,h=7)
            plt.show()
            
            redo = input("next?[y]y/n")
            
            if (redo == "n"):
                break

    

