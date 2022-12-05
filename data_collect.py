# Importing Libraries
import serial
import struct
import time
import csv
import os

import matplotlib.pyplot as plt

COM_PORT = 'COM7'    # 指定通訊埠名稱
BAUD_RATES = 500000    # 設定傳輸速率
ser = serial.Serial(COM_PORT, BAUD_RATES)
interval = 3

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

try:
    while True:
        number = input("手勢編號 :")

        if (number.isdigit() == False):
            print("not a number")
            continue
        
        print("手勢 : ",gestures[int(number)])
        
        s_number = input("樣本數量 :")
        
        if (s_number.isdigit() == False):
            print("not a number")
            continue
        
        print("數量 : ",s_number)
        
        i = 0
        while i < int(s_number):
            print("資料:",i+1)

            data = []
            seconds = time.time()
            s = 0
            ser.reset_input_buffer()
            while time.time() - seconds < interval:   
                while ser.in_waiting >= 1 and s < 3030 :
                    if ser.read() == b'\r' :
                        s += 1
                        if ser.read() == b'\n' :
                            data_raw = ser.read(6)
                            data.append(list(data_raw))
    
    
            print("資料總數:", s)
            
            fig = plt.figure()
            plt.plot(data)
            fig.set_size_inches(w=19,h=7)
            plt.show()
            
            redo = input("資料正確?[y] (y/n)")
    
            if (redo == "n"):
                continue
            
            i += 1 
            
            #------------check directory------------
            filepath = 'training_data/' + str(number)
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            #------------edit csv file--------------
            filename = filepath + '/' + str(number) + '_' + str(int((time.time()))) + '.csv'
            with open(filename, 'w+', newline='') as csvfile:
                # 建立 CSV 檔寫入器
                writer = csv.writer(csvfile)
                # 寫入一列資料
                writer.writerow(['a0', 'a1', 'a2', 'a3', 'a4', 'a5'])
                writer.writerows(data)
                
                
        print("手勢 : (", number, ")", gestures[int(number)]," ,數量 : ",s_number, " 已完成" )


except KeyboardInterrupt:
    ser.close()
    print('End')
