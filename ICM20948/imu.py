import time
import board
import adafruit_icm20x
import numpy as np
i2c = board.I2C()  # uses board.SCL and board.SDA
icm = adafruit_icm20x.ICM20948(i2c)






def computeOrientation(imu):
   """ Computes roll, pitch and yaw

   The function uses accelerometer and magnetometer values
   to estimate roll, pitch and yaw. These values could be 
   having some noise, hence look at kalman and madgwick 
   filters in filters folder to get a better estimate.
   
   """

   roll = np.arctan2(imu.acceleration[1], imu.acceleration[2] + 0.05*imu.acceleration[0])
   pitch = np.arctan2(-1*imu.acceleration[0], np.sqrt(np.square(imu.acceleration[1]) + np.square(imu.acceleration[2]) ))
   magLength = np.sqrt(np.square(imu.magnetic).sum())
   normmagnetic = imu.magnetic/magLength
   yaw = np.arctan2(np.sin(roll)*normmagnetic[2] - np.cos(roll)*normmagnetic[1],\
            np.cos(pitch)*normmagnetic[0] + np.sin(roll)*np.sin(pitch)*normmagnetic[1] \
            + np.cos(roll)*np.sin(pitch)*normmagnetic[2])

   rollDeg = np.degrees(roll)
   pitchDeg = np.degrees(pitch)
   yawDeg = np.degrees(yaw)

   return (rollDeg,pitchDeg,yawDeg)



while True:
    
   

   print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (icm.acceleration))
   print("Gyro X:%.2f, Y: %.2f, Z: %.2f rads/s" % (icm.gyro))
   print("Magnetometer X:%.2f, Y: %.2f, Z: %.2f uT" % (icm.magnetic))

   print("Orientation X:%.2f, Y: %.2f, Z: %.2f Deg" % (computeOrientation(icm)))


   print("")
   time.sleep(0.5)