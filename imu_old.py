import time
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

mpu = MPU9250(
    address_ak=AK8963_ADDRESS, 
    address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
    address_mpu_slave=None, 
    bus=1,
    gfs=GFS_1000, 
    afs=AFS_8G, 
    mfs=AK8963_BIT_16, 
    mode=AK8963_MODE_C100HZ)
mpu.calibrateMPU6500() # Calibrate sensors
mpu.configure() # Apply the settings to the registers.

while True:

	x_g = round(mpu.readAccelerometerMaster()[0],3)
	y_g = round(mpu.readAccelerometerMaster()[1],3)	
	z_g = round(mpu.readAccelerometerMaster()[2],3)
	
	x_d = round(mpu.readGyroscopeMaster()[0],3)
	y_d = round(mpu.readGyroscopeMaster()[1],3)	
	z_d = round(mpu.readGyroscopeMaster()[2],3)
	
	
	x_mt = round(mpu.readMagnetometerMaster()[0],3)
	y_mt = round(mpu.readMagnetometerMaster()[1],3)	
	z_mt = round(mpu.readMagnetometerMaster()[2],3)	
	
	temp = (mpu.readTemperatureMaster() * 9/5) + 32
	
	print("Accelerometer:   Gyroscope:   Magnetometer:   Temp:   \n")
	print(str(x_g) + ' '*13 + str(x_d) + ' ' * 10 + str(x_mt) + ' ' * 12 + str(temp))
	print(str(y_g) + ' '*13 + str(y_d) + ' ' * 10 + str(y_mt))
	print(str(z_g) + ' '*13 + str(z_d) + ' ' * 10 + str(z_mt))
	time.sleep(1)
    #print("Accelerometer: \n", mpu.readAccelerometerMaster())
    # g (1g = 9.80665 m/sÂ²)
    #print("Gyroscope", mpu.readGyroscopeMaster())
    # degrees per second (Â°/s)
    #print("Magnetometer", mpu.readMagnetometerMaster())
    # microtesla (Î¼T)
    #print("Temperature", mpu.readTemperatureMaster())
    #print("\n")

