#%%
import os
import pandas as pd
import numpy as np

import scipy as sp
from scipy import signal

from sklearn.model_selection import train_test_split
from keras.utils import np_utils

from keras.models import Sequential
from keras.layers import Dense,Dropout,Flatten,Conv2D,MaxPooling2D
from tensorflow import keras
from tensorflow.keras import layers

import matplotlib.pyplot as plt
#%%
#===========================資料讀取===========================
path = "./training_data"
gestures=os.listdir(path) # 路徑下的所有檔案

'''
for gesture in gestures:
    print (gesture)
'''


mode = 1 #0 for emg + fsr ,1 for emg 

if mode == 1:
    size = 4
else :
    size = 6

Y_data = np.array([]) 
X_data = np.zeros((0,3,500,size))#先建立X_data的空架構，預設圖片大小500x6

#%%
#===========================EMG濾波函數========================
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

#%%
#===========================讀取資料===========================
for gesture in gestures:
    path_dir = os.path.join(path, gesture) # 路徑 + 手勢編號
    if os.path.isdir(path_dir): # 如果這個檔案是資料夾
        fds=os.listdir(path_dir) # 手勢編號下的所有檔案
        
        for j in range(len(fds)):  # 相同手勢編號下的每個檔案
            csv = fds[j] # 獲得csv檔名
            path_csv = os.path.join(path_dir, csv) #csv檔路徑
            df = pd.read_csv( path_csv)#讀取csv檔
            
            steps = np.zeros((0,500,size))
            
            #Y_data.append
            Y_data = np.append(Y_data, gesture) #把label加入Y_data
            
            for k in range(1,4):
                
                
                    
                #X_data.append
                df1 = df.iloc[250*k:500+250*k]#從這個class開始第250筆資料後面取500
                    
                #DataFrame to numpy
                df2 = df1.to_numpy() #DataFrame轉成Numpy array
                
                #EMG filter
                EMG = emg_filter(df2)
                EMG1 = EMG[:,6-size:6].reshape(1,500,size) #因為要加入X_train裡面所以shape要一樣
                
                steps = np.concatenate((steps, EMG1))
                
            steps = steps.reshape(1,3,500,size)    
            
            X_data = np.concatenate((X_data, steps)) #新的資料加入(n, 3 , 500, 6)

#%%                           
#===========================分割資料===========================                        
#看資料型態
print(X_data.shape)
print(Y_data.shape)
print(Y_data[:20])

#%% 
#資料型態調整成可放入CNN架構型態
X_data = X_data.reshape(-1, 3, 500, size, 1) #CNN有ＲＧＢ值
#Y_data = Y_data.astype(int) - 1 #沒有0的資料Onehot會補0，造成資料對不上，所以減1
#print(Y_data[:20])

#分割資料
X_train, X_test, Y_train, Y_test = train_test_split(X_data, Y_data, test_size=0.5, random_state=369)  
print(X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)

#Onehot
Y_train_onehot = np_utils.to_categorical(Y_train)
Y_test_onehot = np_utils.to_categorical(Y_test)

#%%
#===========================模型建立=========================== 
CNN = keras.Sequential(name='CNN')



#抓取特徵
#用Convolution 2D的就可 參數(filters, kernal_size)
CNN.add(layers.TimeDistributed(layers.Conv2D(16, (20,1), strides = (10,1), activation='relu', input_shape=( 3, 500, size, 1))) )
#Pooling 
CNN.add(layers.TimeDistributed(layers.MaxPooling2D((20,1))))
#第二次Convolution 就不用再input 
CNN.add(layers.TimeDistributed(layers.Conv2D(32, (1,2),strides= (1,2), activation='relu')))
#第二次Max
CNN.add(layers.TimeDistributed(layers.MaxPooling2D((2,1))) )

#壓平 4x4x32 = 512
CNN.add(layers.TimeDistributed((layers.Flatten())))
#隱藏層 Dense 神經元數量 512>50>10 因為最後是10類
CNN.add(layers.LSTM(50))
#隨機捨棄神經元，避免overfitting
CNN.add(Dropout(0.7))
#輸出層 分類用softmax
CNN.add(layers.Dense(10,activation='softmax'))


input_shape=(None, 3, 500, size, 1)
CNN.build(input_shape)  

#做連結圖
keras.utils.plot_model(CNN, show_shapes=True)

# model.complie
CNN.compile(optimizer='Adam',
      loss='categorical_crossentropy',
      metrics=['accuracy'])

#%%
#===========================訓練模型=========================== 
train_history=CNN.fit(x=X_train, 
                      y=Y_train_onehot,
                      validation_split=0.1, 
                      epochs=60, 
                      batch_size=10, 
                      verbose=2)

#%%
#===========================Learning Curve=========================== 
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6,12))

# Plot training & validation accuracy values
ax1.plot(train_history.history['accuracy'])
ax1.plot(train_history.history['val_accuracy'])
ax1.set_title('Accuracy')
ax1.set(ylabel='Accuracy', xlabel='Epoch')
ax1.legend(['Train', 'Valid'], loc='upper left')

# Plot training & validation loss values
ax2.plot(train_history.history['loss'])
ax2.plot(train_history.history['val_loss'])
ax2.set_title('Model loss')
ax2.set(ylabel='Loss', xlabel='Epoch')
ax2.legend(['Train', 'Valid'], loc='upper right')

# plt.savefig('train_history.png', dpi=96)  # <-- save plot
plt.show()

#%%
#===========================測試模型精準度=========================== 
scores = CNN.evaluate(X_test, Y_test_onehot)
print('Test Accuracy:', scores[1] )

prediction=CNN.predict(X_test)
classes_x=np.argmax(prediction,axis=1)

print(classes_x[:20])
print(Y_test[:20])

pd.crosstab(Y_test,classes_x,
            rownames=['label'],colnames=['predict'])

#%%
#===========================儲存模型=========================== 
CNN.save('my_model.h5')
