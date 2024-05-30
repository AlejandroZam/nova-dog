import config
import platform
import smbus
import time
from time import sleep
import busio
import board
import numpy as np
# cfg = config.getConfigVals()


# print(cfg.WIT_SAVE)
# print(cfg.WIT_CALSW)
# print(cfg.WIT_SAVECONF)
# print(cfg.WIT_UNLOCK)



RRATEDataDef = {  0x01:0.2,
                  0x02:0.5,
                  0x03:1.0,
                  0x04:2,
                  0x05:5,
                  0x06:10.0,
                  0x07:20.0,
                  0x08:50.0,
                  0x09:100.0,
                  0x0B:200.0,
                  0x0C:'single return',
                  0x0D:'no return'
                }
BAUDDataDef = {   0x01:4800,
                  0x02:9600,
                  0x03:19200,
                  0x04:38400,
                  0x05:57600,
                  0x06:115200,
                  0x07:230400,
                  0x08:460800, #（Only supportsWT931/JY931/HWT606/HWT906）
                  0x09:921600 # （Only supportsWT931/JY931/HWT606/HWT906）
                }
DataTypeDef = {   0x01:('TIME',0x50),
                  0x02:('ACC',0x51),
                  0x04:('GYRO',0x52),
                  0x08:('ANGLE',0x53),
                  0x10:('MAG',0x54),
                  0x20:('PORT',0x55),
                  0x40:('PRESS',0x56),
                  0x80:('GPS',0x57),
                  0x100:('VELOCITY',0x58),
                  0x200:('QUATER',0x59),
                  0x400:('GSA',0x5A)
                }

class WT901:
   
   rate = 0.0
   baud = 0.0
   datacontent = []
   
   magX = 0.0
   magY = 0.0
   magZ = 0.0
   
   accelX = 0.0
   accelY = 0.0
   accelZ = 0.0
   
   angVelX = 0.0 
   angVelY = 0.0
   angVelZ = 0.0
   
   roll = 0.0
   pitch = 0.0
   yaw = 0.0
   
   temp= 0.0
   
   def __init__(self, bus, address):
      self.cfg = config.getConfigVals()
      self.Address = address
      self.Bus = bus
      self.read_IICADDR()
      self.read_BAUD()
      self.read_RRATE()
      self.read_RSW()
  
   def readRegisters(self,subaddress,count,raw=True):
      data = self.Bus.read_i2c_block_data(self.Address, subaddress, count)
      if raw:
         return data
      else:
         return data

   # def writeRegister(self,subaddress,byte):
   #    self.Bus.write_byte(self.Address,subaddress, byte)
      
   # def writeRegister(self,subaddress,word):
   #    self.Bus.write_word_data(self.Address,subaddress, word)
      
   # def writeRegister(self,subaddress,bytearray):
   #    self.Bus.write_i2c_block_data(self.Address,subaddress, bytearray)
      

      
      
   # def writeRegister(self,subaddress,data):
   #    self.Bus.write_byte_data(self.Address,subaddress, data)

   def read_RSW(self):
      data = self.readRegisters(self.cfg.WIT_RSW,2)
      low0 = data[0]
      high0 = data[1]
      data = [(high0<<8) | low0 ]
      
      for k,v in DataTypeDef.items():
         if k & data[0]:
            self.datacontent.append(v)
      
   def read_RRATE(self):
      data = self.readRegisters(self.cfg.WIT_RRATE,1)
      self.rate = RRATEDataDef[data[0]]
   
   def read_BAUD(self):
      data = self.readRegisters(self.cfg.WIT_BAUD,1)
      self.baud = BAUDDataDef[data[0]]
   
   def read_IICADDR(self):
      data = self.readRegisters(self.cfg.WIT_IICADDR,1)
      self.Address = data[0]
   
   def read_Mag(self,verbose=False):
      datax = self.readRegisters(self.cfg.WIT_HX,2)
      low0 = datax[0]
      high0 = datax[1]
      datax = [(high0<<8) | low0 ]
      self.magX = datax[0]
      datay = self.readRegisters(self.cfg.WIT_HY,2)
      low0 = datay[0]
      high0 = datay[1]
      datay = [(high0<<8) | low0 ]
      self.magY = datay[0]
      
      dataz = self.readRegisters(self.cfg.WIT_HZ,2)
      low0 = dataz[0]
      high0 = dataz[1]
      dataz = [(high0<<8) | low0 ]
      self.magZ = dataz[0]
      
      if verbose:
         print('magnetic field x dir')
         print('[{}]'.format(', '.join(hex(x) for x in datax)))
         print('[{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in datax)))
         print(self.magX)
         
         print('magnetic field y dir')
         print('[{}]'.format(', '.join(hex(x) for x in datay)))
         print('[{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in datay)))
         print(self.magY)
         
         print('magnetic field z dir')
         print('[{}]'.format(', '.join(hex(x) for x in dataz)))
         print('[{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in dataz)))
         print(self.magZ)
         
   def read_Acceleration(self,verbose=False):
      datax = self.readRegisters(self.cfg.WIT_AX,2)
      low0 = datax[0]
      high0 = datax[1]
      datax = [(high0<<8) | low0 ]
      self.accelX = datax[0]/32768*16*(9.8)
      
      datay = self.readRegisters(self.cfg.WIT_AY,2)
      low0 = datay[0]
      high0 = datay[1]
      datay = [(high0<<8) | low0 ]
      self.accelY = datay[0]/32768*16*(9.8)
      
      dataz = self.readRegisters(self.cfg.WIT_AZ,2)
      low0 = dataz[0]
      high0 = dataz[1]
      dataz = [(high0<<8) | low0 ]
      self.accelZ = dataz[0]/32768*16*(9.8)
  
      if verbose:
         print('acceleration x dir')
         print('[{}]'.format(', '.join(hex(x) for x in datax)))
         print('[{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in datax)))
         print(self.accelX)

         print('acceleration y dir')
         print('[{}]'.format(', '.join(hex(x) for x in datay)))
         print('[{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in datay)))
         print(self.accelY)

         print('acceleration z dir')
         print('[{}]'.format(', '.join(hex(x) for x in dataz)))
         print('[{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in dataz)))
         print(self.accelZ)
      
   def read_AngularVelocity(self,verbose=False):
      datax = self.readRegisters(self.cfg.WIT_GX,2)
      low0 = datax[0]
      high0 = datax[1]
      datax = [(high0<<8) | low0 ]
      self.angVelX = datax[0]/32768*2000
      
      datay = self.readRegisters(self.cfg.WIT_GY,2)
      low0 = datay[0]
      high0 = datay[1]
      datay = [(high0<<8) | low0 ]
      self.angVelY = datay[0]/32768*2000
      
      dataz = self.readRegisters(self.cfg.WIT_GZ,2)
      low0 = dataz[0]
      high0 = dataz[1]
      dataz = [(high0<<8) | low0 ]
      self.angVelZ = dataz[0]/32768*2000
      
      if verbose:
         print('angular velocity x dir')
         print('[{}]'.format(', '.join(hex(x) for x in datax)))
         print('[{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in datax)))
         print(self.angVelX)

         print('angular velocity y dir')
         print('[{}]'.format(', '.join(hex(x) for x in datay)))
         print('[{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in datay)))
         print(self.angVelY)
         
         print('angular velocity z dir')
         print('[{}]'.format(', '.join(hex(x) for x in dataz)))
         print('[{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in dataz)))
         print(self.angVelZ)
      
   def read_Angle(self,verbose=False):
      dataroll = self.readRegisters(self.cfg.WIT_Roll,2)
      low0 = dataroll[0]
      high0 = dataroll[1]
      dataroll = [(high0<<8) | low0 ]
      self.roll = dataroll[0]/32768*180
      
      datapitch = self.readRegisters(self.cfg.WIT_Pitch,2)
      low0 = datapitch[0]
      high0 = datapitch[1]
      datapitch = [(high0<<8) | low0 ]
      self.pitch = datapitch[0]/32768*180
      
      datayaw = self.readRegisters(self.cfg.WIT_Yaw,2)
      low0 = datayaw[0]
      high0 = datayaw[1]
      datayaw = [(high0<<8) | low0 ]
      self.yaw = datayaw[0]/32768*180
      
      
      if verbose:
         print('angle roll dir')
         print('[{}]'.format(', '.join(hex(x) for x in dataroll)))
         print('[{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in dataroll)))
         print(self.roll)
         
         print('angle pitch dir')
         print('[{}]'.format(', '.join(hex(x) for x in datapitch)))
         print('[{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in datapitch)))
         print(self.pitch)

         print('angle yaw dir')
         print('[{}]'.format(', '.join(hex(x) for x in datayaw)))
         print('[{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in datayaw)))
         print(self.yaw)
      
   def read_Temp(self,verbose=False):
      data = self.readRegisters(self.cfg.WIT_TEMP,2)
      low0 = data[0]
      high0 = data[1]
      data = [(high0<<8) | low0 ]
      self.temp = data[0]/100
      if verbose:
      
         print('temp')
         print('[{}]'.format(', '.join(hex(x) for x in data)))
         print('[{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in data)))
         print(self.temp)
      
   def update(self):
      self.read_Acceleration()
      self.read_Angle()
      self.read_AngularVelocity
      self.read_Mag()
      self.read_Temp()
   
address = 0x50
bus = smbus.SMBus(1)

imu = WT901(bus,address)

print(imu.rate)
print(imu.baud)
print(imu.datacontent)
print(imu.Address)

# imu.writeRegister(imu.cfg.WIT_UNLOCK)

value1 = (0x00 <<8) |0x09 
value2 = (0x00 <<8) |0x01 
value3 = (0x00 <<8) |0x00 
value4 = (0x00 <<8) |0x32 
value4 = (0x01 <<8) |0xf4 

imu.Bus.write_i2c_block_data(imu.Address,0x69,[0x88, 0xb5])

# imu.Bus.write_byte_data(imu.Address,imu.cfg.WIT_RRATE,value)

imu.Bus.write_word_data(imu.Address,imu.cfg.WIT_RRATE,value1)
imu.Bus.write_word_data(imu.Address,0x61,value4)
imu.Bus.write_word_data(imu.Address,0x63,value4)

data = imu.readRegisters(0x63,2)
low0 = data[0]
high0 = data[1]
data = [(high0<<8) | low0 ]
print(data)

# data = imu.readRegisters(imu.cfg.WIT_CALSW,2)
# print(data)

# imu.Bus.write_word_data(imu.Address,imu.cfg.WIT_CALSW,value2)
# sleep(5)
# imu.Bus.write_word_data(imu.Address,imu.cfg.WIT_CALSW,value3)
# sleep(5)

# data = imu.readRegisters(imu.cfg.WIT_CALSW,2)
# print(data)

# imu.Bus.write_i2c_block_data(imu.Address,imu.cfg.WIT_RRATE,[value])
# imu.Bus.write_block_data(imu.Address,imu.cfg.WIT_RRATE,[value])
# response1 = imu.Bus.block_process_call(imu.Address,imu.cfg.WIT_RRATE,[value])
# response2 = imu.Bus.process_call(imu.Address,imu.cfg.WIT_RRATE,value)



# print(response1)
# print(response2)
# imu.writeRegister(0x00,imu.cfg.WIT_RPTRT)
# imu.writeRegister(imu.cfg.WIT_SAVECONF)



imu.read_RRATE()
print(imu.rate)

imu.update()
startTime = time.time()
currTime = startTime

while True:
   imu.update()
   
   newTime = time.time()
   dt = newTime - currTime
   currTime = newTime
   print("roll:{0} Pitch:{1} Yaw:{2} ".format(imu.roll, imu.pitch, imu.yaw))

   totTime = currTime - startTime
   if totTime >= 1:
      break
   
   time.sleep(0.01)
# print('ax offset')
# data = imu.readRegisters(imu.cfg.WIT_AXOFFSET,2)
# print('[{}]'.format(', '.join(hex(x) for x in data)))
# print('[{}]'.format(', '.join(bin(x) for x in data)))
# print(data)
# data = np.array(data).astype(np.int16)
# print(data)
# high = data[::2] << 8
# newdata = high + data[1::2]


# print(newdata)
