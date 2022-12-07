import time
import serial

import numpy as np
import scipy as sp
from scipy import signal
import matplotlib.pyplot as plt


from keras.models import Sequential
from keras.layers import Dense,Dropout,Flatten,Conv2D,MaxPooling2D
from tensorflow import keras
from tensorflow.keras import layers

mode = 0 #0 for emg + fsr ,1 for emg 

if mode == 1:
    size = 4
else :
    size = 6

model = keras.models.load_model('my_model.h5')
data = np.zeros((1000,size))

second = time.time()
window = 200
update = False
s = 0
temp = []

gestures = {0:"rest",
            1:"剪刀",
            2:"石頭",
            3:"布",
            4:"手腕:上",
            5:"手腕:下",
            6:"手腕:內",
            7:"手腕:外",
            8:"大拇指",
            9:"雙點",
            10:"放大",
            11:"縮小"}




COM_PORT = 'COM7'    # 指定通訊埠名稱
BAUD_RATES = 500000    # 設定傳輸速率
ser = serial.Serial(COM_PORT, BAUD_RATES)


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



try:
    while True:
        while ser.in_waiting >= 1 and s < window :
            if ser.read() == b'\r' :
                if ser.read() == b'\n' :                    
                    temp_raw = ser.read(6)
                    temp.append(list(temp_raw))
                    s += 1
                    if s == window :
                        update = True
                        
            #print(s)
                        
        if update == True:
            temp = np.array(temp)
            data = np.delete(data, slice(window), axis=0)
            data = np.append(data, temp[:,6-size:6], axis=0)
                        
            pdata = emg_filter(data) 
            
# =============================================================================
#             fig, (plt1, plt2) = plt.subplots(2, 1, figsize=(12,7))
#             plt1.plot(data)
#             plt2.plot(pdata)
#             plt.show()
# =============================================================================
            
            pdata = np.reshape(pdata, (1,1000,size)) 

            prediction = model(pdata).numpy()
            gesture = np.argmax(prediction,axis=1)
            print(gestures[gesture[0]])
            
            #print(time.time()-second)
            #second = time.time()
            
            update = False
            s = 0
            temp = []
        
        
except KeyboardInterrupt:
    ser.close()
    print('KeyboardInterrupt')
    
finally :
    ser.close()
    print('End')
    
    
