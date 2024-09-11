import config
import platform
import smbus
import time
from time import sleep
import busio
import board
import numpy as np
import datetime
import struct

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


def print_data(data,name='data'):
   print(name)
   print('decimal: ' ,data)
   print('hex: [{}]'.format(', '.join(hex(x) for x in data)))
   print('binary: [{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in data)))

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
      # self.read_RSW()

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
      print(datax)
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
      temp_data = [(data[1]<<8) | data[0] ]
      self.tempC = temp_data[0]/100
      self.tempF = (self.tempC * 9/5) + 32
      if verbose:
         print('temp')
         print('[{}]'.format(', '.join(hex(x) for x in data)))
         print('[{}]'.format(', '.join(bin(x)[2:].zfill(16) for x in data)))
         print(self.tempC)

   def unlock(self):
      self.Bus.write_i2c_block_data(self.Address,0x69,[0x88, 0xb5])
      sleep(0.5)

   def save(self):
      self.Bus.write_word_data(self.Address,self.cfg.WIT_SAVE,SAVE_PARAM)
      sleep(0.5)

   def writeRegisters(self,regAddress,rawvalue):


      if type(rawvalue) == list:
         if len(rawvalue)==2:
            value = (rawvalue[0]<<8) | rawvalue[1]
         else:
            print('error: value is not 2 bytes')
            print(rawvalue)
            return -1
      else:
         value = rawvalue

      return self.Bus.write_word_data(self.Address,regAddress,value)

   def set_Time(self):
      t = datetime.datetime.now()

      yy = int(t.year-2000)
      mm = int(t.month)

      yymm = struct.pack('>h',(yy << 8) | mm)
      self.writeRegisters(self.cfg.WIT_YYMM,struct.unpack('<h',yymm)[0])

      dd = t.day
      hh = t.hour

      ddhh = struct.pack('>h',(dd << 8) | hh)
      self.writeRegisters(self.cfg.WIT_DDHH,struct.unpack('<h',ddhh)[0])


      mm = t.minute
      ss = t.second

      mmss = struct.pack('>h',(mm << 8) | ss)
      self.writeRegisters(self.cfg.WIT_MMSS,struct.unpack('<h',mmss)[0])

      milisec = int(t.microsecond / 1000)
      ms = struct.pack('>h',milisec)

      self.writeRegisters(self.cfg.WIT_MS,struct.unpack('<h',ms)[0])

   def get_Time(self):

      datayymm = self.readRegisters(self.cfg.WIT_YYMM,2)

      year = datayymm[0] + 2000
      month = datayymm[1]

      dataddhh = self.readRegisters(self.cfg.WIT_DDHH,2)

      day = dataddhh[0]
      hour = dataddhh[1]


      datammss = self.readRegisters(self.cfg.WIT_MMSS,2)


      min = datammss[0]
      sec = datammss[1]

      datams = self.readRegisters(self.cfg.WIT_MS,2)
      ms = [(datams[0]<<8) | datams[1] ][0]


      # print('year: ',year,' month: ', month,' day: ', day,' hour: ', hour,' min: ',min,' sec: ',sec,' ms: ',ms)


   def set_Gyro_cal_time(self,val):
      temp = struct.pack('>h',val)
      self.writeRegisters(self.cfg.WIT_GYROCALTIME,struct.unpack('>h',temp)[0])
      sleep(0.5)


   def set_Accel_filt(self,val):
      temp = struct.pack('>h',val)
      self.writeRegisters(self.cfg.WIT_ACCFILT,struct.unpack('>h',temp)[0])
      sleep(0.5)

   def set_Filt_k(self,val):
      temp = struct.pack('>h',val)
      self.writeRegisters(self.cfg.WIT_FILTK,struct.unpack('>h',temp)[0])
      sleep(0.5)

   def set_Rate(self,val):
      temp = struct.pack('>h',val)
      self.writeRegisters(self.cfg.WIT_RRATE,struct.unpack('>h',temp)[0])
      sleep(0.5)



   def run_Calibration(self,val):

      if type(val) == str:
         try:
            inputval = CALSW[val]
         except:
            return False
      elif type(val) == int:
         inputval = val
      else:
         return False         
      temp = struct.pack('>h',inputval)
      print_data(struct.unpack('<h',temp))
      self.writeRegisters(self.cfg.WIT_FILTK,struct.unpack('<h',temp)[0])


      if inputval == 1:
         sleep(6)
      elif inputval == 7:
         sleep(10)
      elif inputval == 9:
         sleep(6)
      else:
         sleep(2)

      return True



   def update(self):
      self.read_RSW()
      print(self.datacontent)
      self.set_Time()
      self.read_Acceleration()
      self.read_Angle()
      self.read_AngularVelocity
      self.read_Mag()
      self.read_Temp()
      self.datacontent = []

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

imu.set_Gyro_cal_time(500)
imu.set_Accel_filt(500)
imu.set_Filt_k(30)

imu.set_Rate(0x0b)


imu.writeRegisters(imu.cfg.WIT_AXIS6,0x00)
sleep(0.5)


# imu.writeRegisters(imu.cfg.WIT_AXIS6,0x00)
# sleep(0.5)

# imu.run_Calibration('NORMAL')
# imu.run_Calibration('CALGYROACC')
# imu.run_Calibration('CALMAGMM')


imu.set_Time()
imu.save()


# imu.read_RRATE()
# print('set rate to: ',imu.rate)


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



# imu.read_RSW()


imu.update()

imu.get_Time()

print(imu.datacontent)


startTime = time.time()
currTime = startTime

print("roll:{0} Pitch:{1} Yaw:{2} ".format(imu.roll, imu.pitch, imu.yaw))

print("angular_vel_X:{0} angular_vel_Y:{1} angular_vel_Z:{2} ".format(imu.angVelX, imu.angVelY, imu.angVelZ))

print("accel_X:{0} accel_Y:{1} accel_Z:{2} ".format(imu.accelX, imu.accelY, imu.accelZ))

print("mag_X:{0} mag_Y:{1} mag_Z:{2} ".format(imu.magX, imu.magY, imu.magZ))

print("temp:{0} ".format(imu.tempF))






while True:
   imu.update()

   newTime = time.time()
   dt = newTime - currTime
   currTime = newTime
   print(imu.datacontent)
   print("roll:{0} Pitch:{1} Yaw:{2} ".format(imu.roll, imu.pitch, imu.yaw))

   print("angular_vel_X:{0} angular_vel_Y:{1} angular_vel_Z:{2} ".format(imu.angVelX, imu.angVelY, imu.angVelZ))

   print("accel_X:{0} accel_Y:{1} accel_Z:{2} ".format(imu.accelX, imu.accelY, imu.accelZ))

   print("mag_X:{0} mag_Y:{1} mag_Z:{2} ".format(imu.magX, imu.magY, imu.magZ))

   print("temp:{0} ".format(imu.tempF))


   totTime = currTime - startTime
   if totTime >= 10:
      break

   time.sleep(0.1)




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
