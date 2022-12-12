import serial, argparse
import numpy as np
from time import sleep
from collections import deque

import matplotlib.pyplot as plt 
import matplotlib.animation as animation

    
# plot class
class AnalogPlot:
  # constr
  def __init__(self, strPort, maxLen, channel_num=6):
      # open serial port
      self.ser = serial.Serial(strPort, 1000000)
      self.lines = []
      self.channel_num = channel_num
      for _ in range(channel_num):
        self.lines.append(deque([0.0]*maxLen))

    #   self.ax = deque([0.0]*maxLen)
    #   self.ay = deque([0.0]*maxLen)
    #   self.az = deque([0.0]*maxLen)
      self.maxLen = maxLen

  # add to buffer
  def addToBuf(self, buf, val):
      if len(buf) < self.maxLen:
          buf.append(val)
      else:
          buf.pop()
          buf.appendleft(val)

  # add data
  def add(self, data):
      assert(len(data) == self.channel_num)
      for i in range(self.channel_num):
        self.addToBuf(self.lines[i], data[i])
    #   self.addToBuf(self.ax, data[0])
    #   self.addToBuf(self.ay, data[1])
    #   self.addToBuf(self.az, data[2])

  # update plot
  def update(self, frameNum, lines, a0, __):
      try:
        #   line = self.ser.readline()
          print(a0)
          line = self.ser.read(3)
          data = [line[i:i+1] for i in range(0, len(line), 1)]
          data = [ord(val) for val in data]
          
          print(data)
          # print data
          if(len(data) == self.channel_num):
              self.add(data)
              for i in range(self.channel_num):
                lines[i].set_data(range(self.maxLen), self.lines[i])
            #   a0.set_data(range(self.maxLen), self.ax)
            #   a1.set_data(range(self.maxLen), self.ay)
            #   a2.set_data(range(self.maxLen), self.az)
      except KeyboardInterrupt:
          print('exiting')
      
      return lines[0], 

  # clean up
  def close(self):
      # close serial
      self.ser.flush()
      self.ser.close()    

# main() function
def main():
  # create parser
  parser = argparse.ArgumentParser(description="LDR serial")
  # add expected arguments
  parser.add_argument('--port', dest='port', required=True)
  
  #strPort = '/dev/tty.usbserial-A7006Yqh'
  strPort = 'COM3'

  print('reading from serial port %s...' % strPort)

  # plot parameters
  channel_num = 3
  analogPlot = AnalogPlot(strPort, 100, channel_num)

  print('plotting data...')

  # set up animation
  fig = plt.figure()
  ax = plt.axes(xlim=(0, 100), ylim=(0, 1023))
  lines = []
  for i in range(channel_num):
    lines.append(ax.plot([], [])[0])
#   a0, = ax.plot([], [])
#   a1, = ax.plot([], [])
#   a2, = ax.plot([], [])
  anim = animation.FuncAnimation(fig, analogPlot.update, 
                                 fargs=(lines), 
                                 interval=50)

  # show plot
  plt.show()
  
  # clean up
  analogPlot.close()

  print('exiting.')
  

# call main
if __name__ == '__main__':
  main()