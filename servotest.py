from adafruit_pca9685 import PCA9685
import time
import board
from adafruit_motor.servo import Servo



class DS3218():
   
   pulse_width_min = 500
   pulse_width_max = 2500
   physical_deg_min = 0
   physical_deg_max = 270
   operating_freq_min = 50
   operating_freq_max = 330
   
   def angle_to_pw_usec(self,angle):
      return self.pulse_width_min + ((self.pulse_width_max-self.pulse_width_min)*angle/self.physical_deg_max)
   # Operating Voltage:            5V           |  6.8V
   # Idle current(at stopped):     4mA          |  5mA  
   # Operating speed (at no load): 0.16 sec/60° |  0.14sec/60°
   # Stall torque (at locked):     18 kg-cm     |  21.5 kg-cm
   # Stall current (at locked):    1.8A         |  2.2A

   # Control System:           PWM(Pulse width modification)
   # Pulse width range:        500～2500µsec
   # Neutral position:         1500µsec
   # Running degree:           180° or 270°(when 500～2500 μ sec)
   # Dead band width:          3 µsec
   # Operating frequency:      50-330Hz
   # Rotating direction:       Counterclockwise (when 500～2500 µsec)

   def __init__(self):
      pass

class Shoulder(Servo,DS3218):
   
   neutralAngle = 135

   def __init__(self, arm=None, *args, **kwargs):
      self.arm = arm
      if arm=='left':
         self.minAngle = self.neutralAngle - 60
         self.maxAngle = self.neutralAngle + 60
      elif arm=='right':
         self.minAngle = self.neutralAngle + 60
         self.maxAngle = self.neutralAngle - 60
      else:
         print('invalid arm set type')
      super(Shoulder,self).__init__(
         min_pulse=self.pulse_width_min,
         max_pulse=self.pulse_width_max,
         actuation_range = self.physical_deg_max,
         *args, **kwargs)
      
   def setAngle(self,angle):
      if self.arm =='left':
         if angle <self.minAngle or angle >self.maxAngle:
            raise ValueError('Angle '+ str(angle) + ' is out of bounds for shoulder joint')
         else:
            self.angle = angle
      elif self.arm =='right':
         if angle >self.minAngle or angle <self.maxAngle:
            raise ValueError('Angle '+ str(angle) + ' is out of bounds for shoulder joint')
         else:
            self.angle = angle
      else:
         raise ValueError('invalid arm side, needs to be "right" or "left"')
      
      
class Thigh(Servo,DS3218):
   
   neutralAngle = 135
   
   def __init__(self, arm=None, *args, **kwargs):
      self.arm = arm
      if arm=='left':
         self.minAngle = self.neutralAngle - 100
         self.maxAngle = self.neutralAngle + 105
      elif arm=='right':
         self.minAngle = self.neutralAngle + 105
         self.maxAngle = self.neutralAngle - 100
      else:
         print('invalid arm set type')
         
      super(Thigh,self).__init__(
         min_pulse=self.pulse_width_min,
         max_pulse=self.pulse_width_max,
         actuation_range = self.physical_deg_max,
         *args, **kwargs)
      
   def setAngle(self,angle):
      if self.arm =='left':
         if angle <self.minAngle or angle >self.maxAngle:
            raise ValueError('Angle '+ str(angle) + ' is out of bounds for thigh joint')
         else:
            self.angle = angle
      elif self.arm =='right':
         if angle >self.minAngle or angle <self.maxAngle:
            raise ValueError('Angle '+ str(angle) + ' is out of bounds for thigh joint')
         else:
            self.angle = angle
      else:
         raise ValueError('invalid arm side, needs to be "right" or "left"')
      
   
class Tibia(Servo,DS3218):
   
   neutralAngle = 135
   
   def __init__(self, arm=None, *args, **kwargs):
      self.arm = arm
      if arm=='left':
         self.minAngle = self.neutralAngle - 50
         self.maxAngle = self.neutralAngle + 75
      elif arm=='right':
         self.minAngle = self.neutralAngle + 75
         self.maxAngle = self.neutralAngle - 50
      else:
         print('invalid arm set type')
         
      super(Tibia,self).__init__(
         min_pulse=self.pulse_width_min,
         max_pulse=self.pulse_width_max,
         actuation_range = self.physical_deg_max, *args, **kwargs)
      
   def setAngle(self,angle):
      if self.arm =='left':
         if angle <self.minAngle or angle >self.maxAngle:
            raise ValueError('Angle '+ str(angle) + ' is out of bounds for tibia joint')
         else:
            self.angle = angle
      elif self.arm =='right':
         if angle >self.minAngle or angle <self.maxAngle:
            raise ValueError('Angle '+ str(angle) + ' is out of bounds for tibia joint')
         else:
            self.angle = angle
      else:
         raise ValueError('invalid arm side, needs to be "right" or "left"')
      
      
class leg():
   
   def __init__(self,shoulder,thigh,tibia):
      pass
   
   def set_offsets(self):
      pass
   
   def pos(self):
      pass
   
i2c = board.I2C()


pca = PCA9685(i2c)

pca.frequency = 50

#  pulse width range = 500 ~ 2500usec
# neutral position = 1500usec
# operating frequency 50- 330hz


# shoulderfl = Shoulder(pwm_out=pca.channels[0],arm='left')
# shoulderfl.setAngle(shoulderfl.maxAngle)
# time.sleep(3)
# shoulderfl.setAngle(shoulderfl.neutralAngle)
# time.sleep(3)
# shoulderfl.setAngle(shoulderfl.minAngle)
# time.sleep(3)
# shoulderfl.setAngle(shoulderfl.neutralAngle)

# shoulderfl = Shoulder(pwm_out=pca.channels[0],arm='right')
# shoulderfl.setAngle(shoulderfl.maxAngle)
# time.sleep(3)
# shoulderfl.setAngle(shoulderfl.neutralAngle)
# time.sleep(3)
# shoulderfl.setAngle(shoulderfl.minAngle)
# time.sleep(3)
# shoulderfl.setAngle(shoulderfl.neutralAngle)

# thighfl = Thigh(pwm_out=pca.channels[0],arm='left')
# thighfl.setAngle(thighfl.maxAngle)
# time.sleep(3)
# thighfl.setAngle(thighfl.neutralAngle)
# time.sleep(3)
# thighfl.setAngle(thighfl.minAngle)
# time.sleep(3)
# thighfl.setAngle(thighfl.neutralAngle)

thighfl = Thigh(pwm_out=pca.channels[0],arm='right')
thighfl.setAngle(thighfl.maxAngle)
time.sleep(3)
thighfl.setAngle(thighfl.neutralAngle)
time.sleep(3)
thighfl.setAngle(thighfl.minAngle)
time.sleep(3)
thighfl.setAngle(thighfl.neutralAngle)

# tibiafl = Tibia(pwm_out=pca.channels[0],arm='left')
# tibiafl.setAngle(tibiafl.maxAngle)
# time.sleep(3)
# tibiafl.setAngle(tibiafl.neutralAngle)
# time.sleep(3)
# tibiafl.setAngle(tibiafl.minAngle)
# time.sleep(3)
# tibiafl.setAngle(tibiafl.neutralAngle)


# tibiafr = Tibia(pwm_out=pca.channels[0],arm='right')
# tibiafr.setAngle(tibiafr.maxAngle)
# time.sleep(3)
# tibiafr.setAngle(tibiafr.neutralAngle)
# time.sleep(3)
# tibiafr.setAngle(tibiafr.minAngle)
# time.sleep(3)
# tibiafr.setAngle(tibiafr.neutralAngle)





pca.deinit()
# tibia1.setAngle(240)

# time.sleep(2)

# tibia1.setAngle(135)
# time.sleep(2)

# tibia1.setAngle(85)
# time.sleep(2)

# tibia1.setAngle(210)
# time.sleep(2)

# tibia1.setAngle(135)
# time.sleep(2)

# tibia1.setAngle(135)
# time.sleep(2)
# tibia1.setAngle(35)

# time.sleep(2)

# shoulder1.setAngle(135)
# time.sleep(2)
# shoulder1.setAngle(75)
# time.sleep(2)
# shoulder1.setAngle(135)
# time.sleep(2)

# servo1 = Servo(pca.channels[0],actuation_range = 270, min_pulse=500, max_pulse=2500)

# neutral = 135
# min = neutral - 60
# max = neutral + 60

# servo1.angle = neutral
# time.sleep(4)

# servo1.angle = min
# time.sleep(4)
# servo1.angle = max
# time.sleep(4)

# servo1.angle = neutral
# time.sleep(4)

