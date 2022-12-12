import time
import serial
import threading
from collections import Counter

import numpy as np
#import scipy as sp
from scipy import signal
#import matplotlib.pyplot as plt


#from keras.models import Sequential
#from keras.layers import Dense,Dropout,Flatten,Conv2D,MaxPooling2D
from tensorflow import keras
#from tensorflow.keras import layers



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


def main(RF, COM_PORT = 'COM7' , BAUD_RATES = 500000, LIST = [0] * 10):

    ser = serial.Serial(COM_PORT, BAUD_RATES)
    
    s = 0
    temp = []
    update = False
    window = 250
    
    
    mode = 0 #0 for emg + fsr ,1 for emg 

    if mode == 1:
        size = 4
    else :
        size = 6
        
    data = np.zeros((1000,size))
    
    model = keras.models.load_model('my_model.h5')
    
    second = time.time()
    

    while RF.is_set():
        
        while ser.in_waiting >= 1 and s < window :
            if ser.read() == b'\r' :
                if ser.read() == b'\n' :                    
                    temp_raw = ser.read(6)
                    temp.append(list(temp_raw))
                    s += 1
                    if s == window :
                        update = True
                        
            #print(s)
                        
        if update == True :    
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
            
            LIST[:-1] = LIST[1:]
            LIST[-1] = gesture[0]
            #print(gestures[gesture[0]])
            
            update = False
            s = 0
            temp = []
            
# =============================================================================
#             print(time.time()-second)
#             second = time.time()
# =============================================================================
            
        
    ser.close()
    print('Model End')
        
if __name__ == "__main__":
    
       
    gestures = {0:"rest",
                1:"剪刀",
                2:"石頭",
                3:"布",
                4:"手腕:上",
                5:"手腕:下",
                6:"手腕:內",
                7:"手腕:外",
                8:"大拇指",
                9:"雙點"}

    COM_PORT = 'COM7'    # 指定通訊埠名稱
    BAUD_RATES = 500000    # 設定傳輸速率
    LIST = [0] * 6
    RF = threading.Event()
    
    model_thread = threading.Thread(target = main, args=(RF, COM_PORT, BAUD_RATES, LIST,))
    
    RF.set()
    model_thread.setDaemon(True)
    model_thread.start()
    try:
        while True :
            show = input("show?")
            time.sleep(2)
            out = Counter(LIST).most_common(1)
            print("show: ",gestures[out[0][0]])
            
    except (KeyboardInterrupt, SystemExit):
        RF.clear()
        model_thread.join()
        print ('KeyboardInterrupt')
        
    finally :
        RF.clear()
        model_thread.join()
        print ('END')

        


