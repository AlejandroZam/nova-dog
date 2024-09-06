from easydict import EasyDict as edict
import numpy as np



def getConfigVals():
   cfg = edict()

   # cfg.WIT_address = 0x50


   cfg.WIT_SAVE       = 0x00       # save current settings
   cfg.WIT_CALSW      = 0x01       # calibrate
   cfg.WIT_RSW        = 0x02       # report data contents
   cfg.WIT_RRATE      = 0x03       # report rate
   cfg.WIT_BAUD       = 0x04       # serial baud rate
   cfg.WIT_AXOFFSET   = 0x05       # X-axis accelerometer offset
   cfg.WIT_AYOFFSET   = 0x06       # Y-axis accelerometer offset
   cfg.WIT_AZOFFSET   = 0x07       # Z-axis accelerometer offset
   cfg.WIT_GXOFFSET   = 0x08       # X-axis angular velocity meter offset
   cfg.WIT_GYOFFSET   = 0x09       # Y-axis angular velocity meter offset
   cfg.WIT_GZOFFSET   = 0x0A       # Z-axis angular velocity meter offset
   cfg.WIT_HXOFFSET   = 0x0B       # X-axis magnetic field meter offset
   cfg.WIT_HYOFFSET   = 0x0C       # Y-axis magnetic field meter offset
   cfg.WIT_HZOFFSET   = 0x0D       # Z-axis magnetic field meter offset
   cfg.WIT_D0MODE     = 0x0E       # D0 mode
   cfg.WIT_D1MODE     = 0x0F       # D1 mode
   cfg.WIT_D2MODE     = 0x10       # D2 mode
   cfg.WIT_D3MODE     = 0x11       # D3 mode
   cfg.WIT_D0PWMH     = 0x12       # D0 PWM lenth of High Level
   cfg.WIT_D1PWMH     = 0x13       # D1 PWM lenth of High Level
   cfg.WIT_D2PWMH     = 0x14       # D2 PWM lenth of High Level
   cfg.WIT_D3PWMH     = 0x15       # D3 PWM lenth of High Level
   cfg.WIT_D0PWMT     = 0x16       # D0 PWM period
   cfg.WIT_D1PWMT     = 0x17       # D1 PWM period
   cfg.WIT_D2PWMT     = 0x18       # D2 PWM period
   cfg.WIT_D3PWMT     = 0x19       # D3 PWM period
   cfg.WIT_IICADDR    = 0x1A       # IIC address
   cfg.WIT_LEDOFF     = 0x1B       # turn off LED
   cfg.WIT_MAGRANGX   = 0x1C      # Magnetic field X calibration range
   cfg.WIT_MAGRANGY   = 0x1D      # Magnetic field Y calibration range
   cfg.WIT_MAGRANGZ   = 0x1E      # Magnetic field Z calibration range
   
   cfg.WIT_BANDWIDTH  = 0x1F      # Bandwidth
   cfg.WIT_GYRORANGE  = 0x20      # Gyro range
   cfg.WIT_ACCRANGE   = 0x21      # Acceleration range

   cfg.WIT_SLEEP      = 0x22       # Sleep
   cfg.WIT_ORIENT     = 0x23       # module install direction
   cfg.WIT_AXIS6      = 0x24       # Algorithm
   
   cfg.WIT_FILTK      = 0x25       # Dynamic filtering
   cfg.WIT_GPSBAUD	 = 0x26       # GPS Baud rate
   cfg.WIT_READADDR	 = 0x27       # Read register
   cfg.WIT_BWSCALE	 = 0x28       # 
   cfg.WIT_MOVETHR	 = 0x28       # 
   cfg.WIT_MOVESTA	 = 0x29       # 
   cfg.WIT_ACCFILT	 = 0x2A       # Acceleration filtering
   cfg.WIT_GYROFILT	 = 0x2B       # Gyro filtering
   cfg.WIT_MAGFILT	 = 0x2C       # Mag filtering
   cfg.WIT_POWONSEND	 = 0x2D       # command start
   cfg.WIT_VERSION	 = 0x2E       # Version number
   cfg.WIT_CCBW	    = 0x2F       # 
   cfg.WIT_YYMM       = 0x30       # year and month
   cfg.WIT_DDHH       = 0x31       # day and hour
   cfg.WIT_MMSS       = 0x32       # minute and second
   cfg.WIT_MS         = 0x33       # milliseconds
   cfg.WIT_AX         = 0x34       # X-axis acceleration
   cfg.WIT_AY         = 0x35       # Y-axis acceleration
   cfg.WIT_AZ         = 0x36       # Z-axis acceleration
   cfg.WIT_GX         = 0x37       # X-axis angular velocity
   cfg.WIT_GY         = 0x38       # Y-axis angular velocity
   cfg.WIT_GZ         = 0x39       # Z-axis angular velocity
   cfg.WIT_HX         = 0x3A       # X-axis magnetic Field
   cfg.WIT_HY         = 0x3B       # Y-axis magnetic Field
   cfg.WIT_HZ         = 0x3C       # Z-axis magnetic Field
   cfg.WIT_Roll       = 0x3D       # X-axis angle
   cfg.WIT_Pitch      = 0x3E       # Y-axis angle
   cfg.WIT_Yaw        = 0x3F       # Z-axis angle
   cfg.WIT_TEMP       = 0x40       # module temperature
   cfg.WIT_D0Status   = 0x41       # D0 port status
   cfg.WIT_D1Status   = 0x42       # D1 port status
   cfg.WIT_D2Status   = 0x43       # D2 port status
   cfg.WIT_D3Status   = 0x44       # D3 port status
   cfg.WIT_PressureL  = 0x45       # pressure low word
   cfg.WIT_PressureH  = 0x46       # pressure high word
   cfg.WIT_HeightL    = 0x47       # height low word
   cfg.WIT_HeightH    = 0x48       # height high word
   cfg.WIT_LonL       = 0x49       # longitude low word
   cfg.WIT_LonH       = 0x4A       # longitude high word
   cfg.WIT_LatL       = 0x4B       # lattitude low word
   cfg.WIT_LatH       = 0x4C       # lattitude high word
   cfg.WIT_GPSHeight  = 0x4D       # GPS height
   cfg.WIT_GPSYAW     = 0x4E       # GPS speed angle
   cfg.WIT_GPSVL      = 0x4F       # GPS speed(ground speed) low word
   cfg.WIT_GPSVH      = 0x50       # GPS speed(ground speed) high word

   # I'm not a specialist and just translated this
   cfg.WIT_Q0         = 0x51       # quaternion Q0
   cfg.WIT_Q1         = 0x52       # quaternion Q1
   cfg.WIT_Q2         = 0x53       # quaternion Q2
   cfg.WIT_Q3         = 0x54       # quaternion Q3

   cfg.WIT_SVNUM		  = 0x55      # Number of satellites
   cfg.WIT_PDOP		  = 0x56      # Position accuracy
   cfg.WIT_HDOP		  = 0x57      # Horizontal accuracy
   cfg.WIT_VDOP		  = 0x58      # Vertical accuracy
   cfg.WIT_DELAYT		  = 0x59      # Alarm delay
   cfg.WIT_XMIN        = 0x5A      # X-axis angle alarm min
   cfg.WIT_XMAX        = 0x5B      # X-axis angle alarm max
   cfg.WIT_BATVAL      = 0x5C      # Supply voltage
   cfg.WIT_ALARMPIN    = 0x5D      # Alarm Pin Mapping
   cfg.WIT_YMIN        = 0x5E      # Y-axis angle alarm min
   cfg.WIT_YMAX        = 0x5F      # Y-axis angle alarm max
   cfg.WIT_GYROZSCALE  = 0x60      # 
   cfg.WIT_GYROCALITHR = 0x61      # Gyro Still Threshold
   cfg.WIT_ALARMLEVEL  = 0x62      # Angle alarm level

   cfg.WIT_GYROCALTIME	  = 0x63   # gyroscope auto calibration
   cfg.WIT_REFROLL		  = 0x64   #
   cfg.WIT_REFPITCH		  = 0x65   #
   cfg.WIT_REFYAW			  = 0x66   #
   cfg.WIT_GPSTYPE        = 0x67   #
   cfg.WIT_TRIGTIME       = 0x68   # Alarm continuous trigger time
   cfg.WIT_KEY            = 0x69   # Unlock
   cfg.WIT_WERROR         = 0x6A   # Gyro change
   cfg.WIT_TIMEZONE       = 0x6B   # GPSTimezone
   cfg.WIT_CALICNT        = 0x6C   #
   cfg.WIT_WZCNT          = 0x6D   #
   cfg.WIT_WZTIME         = 0x6E   # Angular velocity continuous rest time
   cfg.WIT_WZSTATIC       = 0x6F   # Angular velocity integral threshold
   cfg.WIT_ACCSENSOR 	  = 0x70   #485 data response delay
   cfg.WIT_GYROSENSOR 	  = 0x71   #
   cfg.WIT_MAGSENSOR 	  = 0x72   #
   cfg.WIT_PRESSENSOR 	  = 0x73   #
   cfg.WIT_MODDELAY       = 0x74   #
   cfg.WIT_ANGLEAXIS      = 0x75   #
   cfg.WIT_XRSCALE		  = 0x76   #
   cfg.WIT_YRSCALE		  = 0x77   #
   cfg.WIT_ZRSCALE		  = 0x78   #
   cfg.WIT_XREFROLL		  = 0x79   # Roll angle zero reference value
   cfg.WIT_YREFPITCH		  = 0x7A   # pitch angle zero reference value
   cfg.WIT_ZREFYAW		  = 0x7B   # 
   cfg.WIT_ANGXOFFSET	  = 0x7C   #
   cfg.WIT_ANGYOFFSET	  = 0x7D   #
   cfg.WIT_ANGZOFFSET	  = 0x7E   #
   cfg.WIT_NUMBERID1      = 0x7F   # Device No1-2
   cfg.WIT_NUMBERID2      = 0x80   # Device No3-4
   cfg.WIT_NUMBERID3      = 0x81   # Device No5-6
   cfg.WIT_NUMBERID4      = 0x82   # Device No7-8
   cfg.WIT_NUMBERID5      = 0x83   # Device No9-10
   cfg.WIT_NUMBERID6      = 0x84   # Device No11-12
   cfg.WIT_XA85PSCALE     = 0x85   #
   cfg.WIT_XA85NSCALE     = 0x86   #
   cfg.WIT_YA85PSCALE     = 0x87   #
   cfg.WIT_YA85NSCALE     = 0x88   #
   cfg.WIT_XA30PSCALE     = 0x89   #
   cfg.WIT_XA30NSCALE     = 0x8A   #
   cfg.WIT_YA30PSCALE     = 0x8B   #
   cfg.WIT_YA30NSCALE     = 0x8C   #
   cfg.WIT_CHIPIDL        = 0x8D   #

   # cfg.WIT_CONTROL = [0xFF, 0xAA]  # for control usage
   # cfg.WIT_UNLOCK = cfg.WIT_CONTROL + [0x69, 0x88, 0xb5]
   # cfg.WIT_SAVECONF = cfg.WIT_CONTROL + [ cfg.WIT_SAVE, 0x00, 0x00]
   # cfg.WIT_SETCALI = cfg.WIT_CONTROL + [ cfg.WIT_CALSW, 0x00, 0x00]
   # cfg.WIT_INSTALL = cfg.WIT_CONTROL + [ cfg.WIT_DIRECTION, 0x00, 0x00]
   # cfg.WIT_SLEEP = cfg.WIT_CONTROL + [ cfg.WIT_HIBERNATE, 0x01, 0x00]
   # cfg.WIT_ALGAXIS = cfg.WIT_CONTROL + [ cfg.WIT_CHANGEALG, 0x00, 0x00]
   # cfg.WIT_GYROAUTO = cfg.WIT_CONTROL + [ cfg.WIT_GYROAUTOCALI, 0x00, 0x00]
   # cfg.WIT_RPTCONF = cfg.WIT_CONTROL + [ cfg.WIT_RSW, 0x00, 0x00]
   # cfg.WIT_RPTRT = cfg.WIT_CONTROL + [ cfg.WIT_RRATE, 0x00, 0x00]
   # cfg.WIT_BAUDRT = cfg.WIT_CONTROL + [ cfg.WIT_BAUD, 0x00, 0x00]
   # cfg.WIT_AXOFF = cfg.WIT_CONTROL + [ cfg.WIT_AXOFFSET, 0x00, 0x00]
   # cfg.WIT_AYOFF = cfg.WIT_CONTROL + [ cfg.WIT_AYOFFSET, 0x00, 0x00]
   # cfg.WIT_AZOFF = cfg.WIT_CONTROL + [ cfg.WIT_AZOFFSET, 0x00, 0x00]
   # cfg.WIT_GXOFF = cfg.WIT_CONTROL + [ cfg.WIT_GXOFFSET, 0x00, 0x00]
   # cfg.WIT_GYOFF = cfg.WIT_CONTROL + [ cfg.WIT_GYOFFSET, 0x00, 0x00]
   # cfg.WIT_GZOFF = cfg.WIT_CONTROL + [ cfg.WIT_GZOFFSET, 0x00, 0x00]
   # cfg.WIT_HXOFF = cfg.WIT_CONTROL + [ cfg.WIT_HXOFFSET, 0x00, 0x00]
   # cfg.WIT_HYOFF = cfg.WIT_CONTROL + [ cfg.WIT_HYOFFSET, 0x00, 0x00]
   # cfg.WIT_HZOFF = cfg.WIT_CONTROL + [ cfg.WIT_HZOFFSET, 0x00, 0x00]
   # cfg.WIT_D0MODECONF = cfg.WIT_CONTROL + [ cfg.WIT_D0MODE, 0x00, 0x00]
   # cfg.WIT_D1MODECONF = cfg.WIT_CONTROL + [ cfg.WIT_D1MODE, 0x00, 0x00]
   # cfg.WIT_D2MODECONF = cfg.WIT_CONTROL + [ cfg.WIT_D2MODE, 0x00, 0x00]
   # cfg.WIT_D3MODECONF = cfg.WIT_CONTROL + [ cfg.WIT_D3MODE, 0x00, 0x00]
   # cfg.WIT_D0PWMHCONF = cfg.WIT_CONTROL + [ cfg.WIT_D0PWMH, 0x00, 0x00]
   # cfg.WIT_D1PWMHCONF = cfg.WIT_CONTROL + [ cfg.WIT_D1PWMH, 0x00, 0x00]
   # cfg.WIT_D2PWMHCONF = cfg.WIT_CONTROL + [ cfg.WIT_D2PWMH, 0x00, 0x00]
   # cfg.WIT_D3PWMHCONF = cfg.WIT_CONTROL + [ cfg.WIT_D3PWMH, 0x00, 0x00]
   # cfg.WIT_D0PWMTCONF = cfg.WIT_CONTROL + [ cfg.WIT_D0PWMT, 0x00, 0x00]
   # cfg.WIT_D1PWMTCONF = cfg.WIT_CONTROL + [ cfg.WIT_D1PWMT, 0x00, 0x00]
   # cfg.WIT_D2PWMTCONF = cfg.WIT_CONTROL + [ cfg.WIT_D2PWMT, 0x00, 0x00]
   # cfg.WIT_D3PWMTCONF = cfg.WIT_CONTROL + [ cfg.WIT_D3PWMT, 0x00, 0x00]
   # cfg.WIT_IICADDRESS = cfg.WIT_CONTROL + [ cfg.WIT_IICADDR, 0x00, 0x00]
   # cfg.WIT_LED = cfg.WIT_CONTROL + [ cfg.WIT_LEDOFF, 0x00, 0x00]
   # cfg.WIT_GPSBAUDRATE = cfg.WIT_CONTROL + [ cfg.WIT_GPSBAUD, 0x00, 0x00]

   return cfg




# def getConfigVals():
#    cfg = edict()

#    # cfg.WIT_address = 0x50

#    cfg.WIT_CONTROL.address = [0xFF, 0xAA]  # for control usage
#    cfg.WIT_SAVE.address  = 0x00           # save current settings
#    cfg.WIT_CALSW.address = 0x01          # calibrate
#    cfg.WIT_RSW.address  = 0x02            # report data contents
#    cfg.WIT_RSW.description = 'report data contents'
#    cfg.WIT_RRATE.address  = 0x03          # report rate
#    cfg.WIT_BAUD.address  = 0x04           # serial baud rate
#    cfg.WIT_AXOFFSET.address  = 0x05       # X-axis accelerometer offset
#    cfg.WIT_AYOFFSET.address  = 0x06       # Y-axis accelerometer offset
#    cfg.WIT_AZOFFSET.address  = 0x07       # Z-axis accelerometer offset
#    cfg.WIT_GXOFFSET.address  = 0x08       # X-axis angular velocity meter offset
#    cfg.WIT_GYOFFSET.address  = 0x09       # Y-axis angular velocity meter offset
#    cfg.WIT_GZOFFSET.address  = 0x0A       # Z-axis angular velocity meter offset
#    cfg.WIT_HXOFFSET.address  = 0x0B       # X-axis magnetic field meter offset
#    cfg.WIT_HYOFFSET.address  = 0x0C       # Y-axis magnetic field meter offset
#    cfg.WIT_HZOFFSET.address  = 0x0D       # Z-axis magnetic field meter offset
#    cfg.WIT_D0MODE.address  = 0x0E         # D0 mode
#    cfg.WIT_D1MODE.address  = 0x0F         # D1 mode
#    cfg.WIT_D2MODE.address  = 0x10         # D2 mode
#    cfg.WIT_D3MODE.address  = 0x11         # D3 mode
#    cfg.WIT_D0PWMH.address  = 0x12         # D0 PWM lenth of High Level
#    cfg.WIT_D1PWMH.address  = 0x13         # D1 PWM lenth of High Level
#    cfg.WIT_D2PWMH.address  = 0x14         # D2 PWM lenth of High Level
#    cfg.WIT_D3PWMH.address  = 0x15         # D3 PWM lenth of High Level
#    cfg.WIT_D0PWMT.address  = 0x16         # D0 PWM period
#    cfg.WIT_D1PWMT.address  = 0x17         # D1 PWM period
#    cfg.WIT_D2PWMT.address  = 0x18         # D2 PWM period
#    cfg.WIT_D3PWMT.address  = 0x19         # D3 PWM period
#    cfg.WIT_IICADDR.address  =0x1A        # IIC address
#    cfg.WIT_LEDOFF.address  = 0x1B         # turn off LED
#    cfg.WIT_GPSBAUD.address  =0x1C        # GPS connection baud rate

#    cfg.WIT_HIBERNATE.address  = 0x22  # module install direction
#    cfg.WIT_DIRECTION.address  = 0x23  # module install direction
#    cfg.WIT_CHANGEALG.address  = 0x24  # module install direction

#    cfg.WIT_YYMM.address  = 0x30        # year and month
#    cfg.WIT_DDHH.address  = 0x31       # day and hour
#    cfg.WIT_MMSS.address  = 0x32       # minute and second
#    cfg.WIT_MS.address  = 0x33         # milliseconds
#    cfg.WIT_AX.address  = 0x34         # X-axis acceleration
#    cfg.WIT_AY.address  = 0x35         # Y-axis acceleration
#    cfg.WIT_AZ.address  = 0x36         # Z-axis acceleration
#    cfg.WIT_GX.address  = 0x37         # X-axis angular velocity
#    cfg.WIT_GY.address  = 0x38         # Y-axis angular velocity
#    cfg.WIT_GZ.address  = 0x39         # Z-axis angular velocity
#    cfg.WIT_HX.address  = 0x3A         # X-axis magnetic Field
#    cfg.WIT_HY.address  = 0x3B         # Y-axis magnetic Field
#    cfg.WIT_HZ.address  = 0x3C         # Z-axis magnetic Field
#    cfg.WIT_Roll.address  = 0x3D       # X-axis angle
#    cfg.WIT_Pitch.address  = 0x3E     # Y-axis angle
#    cfg.WIT_Yaw.address  = 0x3F        # Z-axis angle
#    cfg.WIT_TEMP.address  = 0x40       # module temperature
#    cfg.WIT_D0Status.address  = 0x41   # D0 port status
#    cfg.WIT_D1Status.address  = 0x42   # D1 port status
#    cfg.WIT_D2Status.address  = 0x43   # D2 port status
#    cfg.WIT_D3Status.address  = 0x44   # D3 port status
#    cfg.WIT_PressureL.address  = 0x45  # pressure low word
#    cfg.WIT_PressureH.address  = 0x46  # pressure high word
#    cfg.WIT_HeightL.address  = 0x47    # height low word
#    cfg.WIT_HeightH.address  = 0x48    # height high word
#    cfg.WIT_LonL.address  = 0x49       # longitude low word
#    cfg.WIT_LonH.address  = 0x4A       # longitude high word
#    cfg.WIT_LatL.address  = 0x4B       # lattitude low word
#    cfg.WIT_LatH.address  = 0x4C       # lattitude high word
#    cfg.WIT_GPSHeight.address  = 0x4D  # GPS height
#    cfg.WIT_GPSYAW.address  = 0x4E     # GPS speed angle
#    cfg.WIT_GPSVL.address  = 0x4F      # GPS speed(ground speed) low word
#    cfg.WIT_GPSVH.address  = 0x50      # GPS speed(ground speed) high word

#    # I'm not a specialist and just translated this
#    cfg.WIT_Q0.address  = 0x51 # quaternion Q0
#    cfg.WIT_Q1.address  = 0x52 # quaternion Q1
#    cfg.WIT_Q2.address  = 0x53 # quaternion Q2
#    cfg.WIT_Q3.address  = 0x54 # quaternion Q3

#    cfg.WIT_GYROAUTOCALI.address = 0x63  # gyroscope auto calibration
   
#    cfg.WIT_UNLOCK.address  = cfg.WIT_CONTROL.address  + [0x69, 0x88, 0xb5]
#    cfg.WIT_SAVECONF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_SAVE.address , 0x00, 0x00]
#    cfg.WIT_SETCALI.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_CALSW.address , 0x00, 0x00]
#    cfg.WIT_INSTALL.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_DIRECTION.address , 0x00, 0x00]
#    cfg.WIT_SLEEP.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_HIBERNATE.address , 0x01, 0x00]
#    cfg.WIT_ALGAXIS.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_CHANGEALG.address , 0x00, 0x00]
#    cfg.WIT_GYROAUTO.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_GYROAUTOCALI.address , 0x00, 0x00]
#    cfg.WIT_RPTCONF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_RSW.address , 0x00, 0x00]
#    cfg.WIT_RPTRT.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_RRATE.address , 0x00, 0x00]
#    cfg.WIT_BAUDRT.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_BAUD.address , 0x00, 0x00]
#    cfg.WIT_AXOFF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_AXOFFSET.address , 0x00, 0x00]
#    cfg.WIT_AYOFF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_AYOFFSET.address , 0x00, 0x00]
#    cfg.WIT_AZOFF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_AZOFFSET.address , 0x00, 0x00]
#    cfg.WIT_GXOFF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_GXOFFSET.address , 0x00, 0x00]
#    cfg.WIT_GYOFF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_GYOFFSET.address , 0x00, 0x00]
#    cfg.WIT_GZOFF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_GZOFFSET.address , 0x00, 0x00]
#    cfg.WIT_HXOFF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_HXOFFSET.address , 0x00, 0x00]
#    cfg.WIT_HYOFF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_HYOFFSET.address , 0x00, 0x00]
#    cfg.WIT_HZOFF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_HZOFFSET.address , 0x00, 0x00]
#    cfg.WIT_D0MODECONF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_D0MODE.address , 0x00, 0x00]
#    cfg.WIT_D1MODECONF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_D1MODE.address , 0x00, 0x00]
#    cfg.WIT_D2MODECONF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_D2MODE.address , 0x00, 0x00]
#    cfg.WIT_D3MODECONF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_D3MODE.address , 0x00, 0x00]
#    cfg.WIT_D0PWMHCONF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_D0PWMH.address , 0x00, 0x00]
#    cfg.WIT_D1PWMHCONF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_D1PWMH.address , 0x00, 0x00]
#    cfg.WIT_D2PWMHCONF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_D2PWMH.address , 0x00, 0x00]
#    cfg.WIT_D3PWMHCONF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_D3PWMH.address , 0x00, 0x00]
#    cfg.WIT_D0PWMTCONF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_D0PWMT.address , 0x00, 0x00]
#    cfg.WIT_D1PWMTCONF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_D1PWMT.address , 0x00, 0x00]
#    cfg.WIT_D2PWMTCONF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_D2PWMT.address , 0x00, 0x00]
#    cfg.WIT_D3PWMTCONF.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_D3PWMT.address , 0x00, 0x00]
#    cfg.WIT_IICADDRESS.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_IICADDR.address , 0x00, 0x00]
#    cfg.WIT_LED.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_LEDOFF.address , 0x00, 0x00]
#    cfg.WIT_GPSBAUDRATE.address  = cfg.WIT_CONTROL.address  + [ cfg.WIT_GPSBAUD.address , 0x00, 0x00]

#    return cfg