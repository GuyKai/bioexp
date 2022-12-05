# Importing Libraries
import serial
import time
import numpy as np

import scipy as sp
from scipy import signal
import matplotlib.pyplot as plt

COM_PORT = 'COM7'    # 指定通訊埠名稱
BAUD_RATES = 500000    # 設定傳輸速率
ser = serial.Serial(COM_PORT, BAUD_RATES)
interval = 3

try:
    while True:
        number = input("gesture number :")

        if (number.isdigit() == False):
            print("not a number")
            continue


        emg = []
        fsr =[]
        seconds = time.time()
        c = 0
        s = 0
        ser.reset_input_buffer()
        while time.time() - seconds < interval :
            #c += 1    
            while ser.in_waiting >= 1 and s < 3030 :
                
                if ser.read() == b'\r' :
                    s += 1
                    if ser.read() == b'\n' :
                        fsr_raw = ser.read(2)
                        emg_raw = ser.read(4)
                        fsr.append(list(fsr_raw))
                        emg.append(list(emg_raw))
                        
                        #t.append(ser.in_waiting)
                        
                        
                

        #print(c)
        #print(s)
        print("資料總數:", s)
            
        data = np.concatenate([fsr, emg], axis=1)
        
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

    
        fig, (plt1, plt2) = plt.subplots(2, 1, figsize=(12,7))
        
        plt1.plot(data)
        plt2.plot(pdata)
        
        plt.show()



except KeyboardInterrupt:
    ser.close()
    print('End')
