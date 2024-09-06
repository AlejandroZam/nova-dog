import config
import platform
import smbus
import time
from time import sleep
import busio
import board
import numpy as np
import datetime


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
CALSW = {   'NORMAL':       0x00,
                  'CALGYROACC':   0x01,
                  'CALMAG':       0x02,
                  'CALALTITUDE':  0x03,
                  'CALANGLEZ':    0x04,
                  'CALACCL':      0x05,
                  'CALACCR':      0x06,
                  'CALMAGMM':     0x07,
                  'CALREFANGLE':  0x08,
                  'CALMAG2STEP':  0x09,
                  'CALHEXAHEDRON':0x12,
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

KEY_UNLOCK = 0xB588
SAVE_PARAM = 0x00
SAVE_SWRST = 0xFF

ORIENT_HERIZONE =	0x00
ORIENT_VERTICLE =	0x01


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

   tempC = 0.0
   tempF = (tempC * 9/5) + 32
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
      self.accelX = datax[0]/32768*16
      if self.accelX >= 16:
         self.accelX -= 2*16

      datay = self.readRegisters(self.cfg.WIT_AY,2)
      low0 = datay[0]
      high0 = datay[1]
      datay = [(high0<<8) | low0 ]
      self.accelY = datay[0]/32768*16
      if self.accelY >= 16:
         self.accelY -= 2*16

      dataz = self.readRegisters(self.cfg.WIT_AZ,2)
      low0 = dataz[0]
      high0 = dataz[1]
      dataz = [(high0<<8) | low0 ]
      self.accelZ = dataz[0]/32768*16
      if self.accelZ >= 16:
         self.accelZ -= 2*16

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
      self.angVelX = datax[0]/32768.0*2000.0
      if self.angVelX >= 2000.0:
         self.angVelX -= 2*2000.0

      datay = self.readRegisters(self.cfg.WIT_GY,2)
      low0 = datay[0]
      high0 = datay[1]
      datay = [(high0<<8) | low0 ]
      self.angVelY = datay[0]/32768.0*2000.0
      if self.angVelY >= 2000.0:
         self.angVelY -= 2*2000.0

      dataz = self.readRegisters(self.cfg.WIT_GZ,2)
      low0 = dataz[0]
      high0 = dataz[1]
      dataz = [(high0<<8) | low0 ]
      self.angVelZ = dataz[0]/32768.0*2000.0
      if self.angVelZ >= 2000.0:
         self.angVelZ -= 2*2000.0

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
      if self.roll >= 180.0:
         self.roll -= 2*180.0

      datapitch = self.readRegisters(self.cfg.WIT_Pitch,2)
      low0 = datapitch[0]
      high0 = datapitch[1]
      datapitch = [(high0<<8) | low0 ]
      self.pitch = datapitch[0]/32768*180
      if self.pitch >= 180.0:
         self.pitch -= 2*180.0

      datayaw = self.readRegisters(self.cfg.WIT_Yaw,2)
      low0 = datayaw[0]
      high0 = datayaw[1]
      datayaw = [(high0<<8) | low0 ]
      self.yaw = datayaw[0]/32768*180
      if self.yaw >= 180.0:
         self.yaw -= 2*180.0

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
      self.tempC = data[0]/100
      self.tempF = (self.tempC * 9/5) + 32
      if verbose:
         print('temp')
         print('[{}]'.format(', '.join(hex(x) for x in data)))
         print('[{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in data)))
         print(self.tempC)

   def unlock(self):
      self.Bus.write_i2c_block_data(self.Address,0x69,[0x88, 0xb5])

   def save(self):
      self.Bus.write_word_data(self.Address,self.cfg.WIT_SAVE,SAVE_PARAM)

   def set_Time(self):
      t = datetime.datetime.now()
      yy = t.year-2000
      print(hex(yy))
      mm = t.month
      print(hex(mm))
      yymm = [yy&0xff,yy >>8,mm&0xff,mm>>8 ]

      print('time yymm')
      print('decimal: ' ,yymm)
      print('hex: [{}]'.format(', '.join(hex(x) for x in yymm)))
      print('binary: [{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in yymm)))
      self.Bus.write_i2c_block_data(self.Address,self.cfg.WIT_YYMM,yymm)

      dd = t.day
      hh = t.hour
      ddhh = [dd&0xff,dd >>8,hh&0xff,hh >>8]

      print('time ddhh')
      print('decimal: ' ,ddhh)
      print('hex: [{}]'.format(', '.join(hex(x) for x in ddhh)))
      print('binary: [{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in ddhh)))
      self.Bus.write_i2c_block_data(self.Address,self.cfg.WIT_DDHH,ddhh)
      # mm = t.minute
      # ss = t.second
      # mmss = [mm&0xff,mm >>8,ss&0xff,ss >>8]

      # print('time mmss')
      # print('decimal: ' ,mmss)
      # print('hex: [{}]'.format(', '.join(hex(x) for x in mmss)))
      # print('binary: [{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in mmss)))

      ms = [t.microsecond]
      print(ms)


 
      # self.Bus.write_i2c_block_data(self.Address,self.cfg.WIT_DDHH,ddhh)

      # self.Bus.write_i2c_block_data(self.Address,self.cfg.WIT_MMSS,mmss)

      # self.Bus.write_i2c_block_data(self.Address,self.cfg.WIT_MS,ms)


   def get_Time(self):

      datayymm = self.readRegisters(self.cfg.WIT_YYMM,4)

      yymmlow0 = datayymm[0]
      yymmhigh0 = datayymm[1]
      yymmlow1 = datayymm[2]
      yymmhigh1 = datayymm[3]

      year = [(yymmhigh0<<8) | yymmlow0 ][0] + 2000
      month = [(yymmhigh1<<8) | yymmlow1 ][0]





      dataddhh = self.readRegisters(self.cfg.WIT_DDHH,4)
      ddhhlow0 = dataddhh[0]
      ddhhhigh0 = dataddhh[1]
      ddhhlow1 = dataddhh[2]
      ddhhhigh1 = dataddhh[3]

      day = [(ddhhhigh0<<8) | ddhhlow0 ]
      hour = [(ddhhhigh1<<8) | ddhhlow1 ]

      print('dataddhh binary: [{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in dataddhh)))
      print(ddhhlow0)
      print(ddhhhigh0)
      print(ddhhlow1)
      print(ddhhhigh1)
      data0 = [(ddhhhigh0<<8) | ddhhlow0 ]
      print('time yy')
      print('decimal: ' ,data0)
      print('hex: [{}]'.format(', '.join(hex(x) for x in data0)))
      print('binary: [{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in data0)))

      data1 = [(ddhhhigh1<<8) | ddhhlow1 ]
      print('time mm')
      print('decimal: ' ,data1)
      print('hex: [{}]'.format(', '.join(hex(x) for x in data1)))
      print('binary: [{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in data1)))

      # datammss = self.readRegisters(self.cfg.WIT_MMSS,4)
      # low0 = datammss[0]
      # high0 = datammss[1]
      # low1 = datammss[2]
      # high1 = datammss[3]

      # min = [(high0<<8) | low0 ]
      # sec = [(high1<<8) | low1 ]

      # datams = self.readRegisters(self.cfg.WIT_MS,2)
      # low0 = datams[0]
      # high0 = datams[1]

      # ms = [(high0<<8) | low0 ]

      print('year: ',year,' month: ', month,' day: ', day,' hour: ', hour)#,' min: ',min,' sec: ',sec,' ms: ',ms)



   def update(self):
      self.read_Acceleration()
      self.read_Angle()
      self.read_AngularVelocity
      self.read_Mag()
      self.read_Temp()

address = 0x50
bus = smbus.SMBus(1)

imu = WT901(bus,address)

# print('rate: ',imu.rate)
# print('baud: ',imu.baud)
# print('datacontent: ',imu.datacontent)
# print('address: ',imu.Address)

# imu.writeRegister(imu.cfg.WIT_UNLOCK)

value1 = (0x00 <<8) |0x09 # rate 100
value2 = (0x07 <<8) |0xe8# yy
value3 = (0x00 <<8) |0x08 # mm
value4 = (0x00 <<8) |0x32
value4 = (0x01 <<8) |0xf4

imu.unlock()

# imu.Bus.write_word_data(imu.Address,imu.cfg.WIT_RRATE,value1) # rate

imu.set_Time()
imu.save()


# imu.read_RRATE()
# print('set rate to: ',imu.rate)

# imu.Bus.write_i2c_block_data(imu.Address,imu.cfg.WIT_YYMM,[0x18,0x00,0x08,0x00]) # yy mm

# data = imu.readRegisters(imu.cfg.WIT_YYMM,4)
# low0 = data[0]
# high0 = data[1]
# low1 = data[2]
# high1 = data[3]

# data0 = [(high0<<8) | low0 ]
# print('time yy')
# print('decimal: ' ,data1)
# print('hex: [{}]'.format(', '.join(hex(x) for x in data0)))
# print('binary: [{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in data0)))

# data1 = [(high1<<8) | low1 ]
# print('time mm')
# print('decimal: ' ,data1)
# print('hex: [{}]'.format(', '.join(hex(x) for x in data1)))
# print('binary: [{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in data1)))


# imu.Bus.write_i2c_block_data(imu.Address,imu.cfg.WIT_DDHH,[0x1e,0x00,0x02,0x00]) # dd hh

# data = imu.readRegisters(imu.cfg.WIT_DDHH,4)
# low0 = data[0]
# high0 = data[1]
# low1 = data[2]
# high1 = data[3]

# data0 = [(high0<<8) | low0 ]
# print('time dd')
# print('decimal: ' ,data0)
# print('hex: [{}]'.format(', '.join(hex(x) for x in data0)))
# print('binary: [{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in data0)))

# data1 = [(high1<<8) | low1 ]
# print('time hh')
# print('decimal: ' ,data1)
# print('hex: [{}]'.format(', '.join(hex(x) for x in data1)))
# print('binary: [{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in data1)))


# imu.Bus.write_i2c_block_data(imu.Address,imu.cfg.WIT_MMSS,[0x0f,0x00,0x1e,0x00]) # mm ss

# data = imu.readRegisters(imu.cfg.WIT_MMSS,4)
# low0 = data[0]
# high0 = data[1]
# low1 = data[2]
# high1 = data[3]

# data0 = [(high0<<8) | low0 ]
# print('time mm')
# print('decimal: ' ,data0)
# print('hex: [{}]'.format(', '.join(hex(x) for x in data0)))
# print('binary: [{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in data0)))

# data1 = [(high1<<8) | low1 ]
# print('time ss')
# print('decimal: ' ,data1)
# print('hex: [{}]'.format(', '.join(hex(x) for x in data1)))
# print('binary: [{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in data1)))

# imu.Bus.write_i2c_block_data(imu.Address,imu.cfg.WIT_MS,[0xf4,0x01]) # mm ss

# data = imu.readRegisters(imu.cfg.WIT_MS,2)
# low0 = data[0]
# high0 = data[1]

# data0 = [(high0<<8) | low0 ]
# print('time ms')
# print('decimal: ' ,data0)
# print('hex: [{}]'.format(', '.join(hex(x) for x in data0)))
# print('binary: [{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in data0)))





# imu.Bus.write_word_data(imu.Address,imu.cfg.WIT_CALSW,[0x03]) # calibrate

# imu.Bus.write_word_data(imu.Address,imu.cfg.WIT_CALSW,[0x02]) # calibrate
# value4 = (0x01 <<8) |0xf4

# value4 = (0x00 <<8) |0x00
# imu.Bus.write_word_data(imu.Address,0x63,value4)
# time.sleep(1)

# value4 = (0x00 <<8) |0x00
# imu.Bus.write_word_data(imu.Address,0x24,value4)

# time.sleep(1)
# value4 = (0x00 <<8) |0x00
# imu.Bus.write_word_data(imu.Address,0x00,value4)

# imu.Bus.write_word_data(imu.Address,0x61,value4)


# data = imu.readRegisters(0x63,2)
# low0 = data[0]
# high0 = data[1]
# data = [(high0<<8) | low0 ]
# print(data)


# data = imu.readRegisters(0x1a,2)
# low0 = data[0]
# high0 = data[1]
# data = [(high0<<8) | low0 ]
# print('address')
# print('decimal: ' ,data)
# print('hex: [{}]'.format(', '.join(hex(x) for x in data)))
# print('binary: [{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in data)))




imu.update()

imu.get_Time()

startTime = time.time()
currTime = startTime

# print("roll:{0} Pitch:{1} Yaw:{2} ".format(imu.roll, imu.pitch, imu.yaw))

# print("angular_vel_X:{0} angular_vel_Y:{1} angular_vel_Z:{2} ".format(imu.angVelX, imu.angVelY, imu.angVelZ))

# print("accel_X:{0} accel_Y:{1} accel_Z:{2} ".format(imu.accelX, imu.accelY, imu.accelZ))

# print("mag_X:{0} mag_Y:{1} mag_Z:{2} ".format(imu.magX, imu.magY, imu.magZ))

# print("temp:{0} ".format(imu.temp))






# while True:
#    imu.update()

#    newTime = time.time()
#    dt = newTime - currTime
#    currTime = newTime
#    print("roll:{0} Pitch:{1} Yaw:{2} ".format(imu.roll, imu.pitch, imu.yaw))

#    print("angular_vel_X:{0} angular_vel_Y:{1} angular_vel_Z:{2} ".format(imu.angVelX, imu.angVelY, imu.angVelZ))

#    print("accel_X:{0} accel_Y:{1} accel_Z:{2} ".format(imu.accelX, imu.accelY, imu.accelZ))

#    print("mag_X:{0} mag_Y:{1} mag_Z:{2} ".format(imu.magX, imu.magY, imu.magZ))

#    print("temp:{0} ".format(imu.tempF))


#    totTime = currTime - startTime
#    if totTime >= 10:
#       break

#    time.sleep(0.1)




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
