import os
import sys
import time
import smbus
import matplotlib.pyplot as plt
from imusensor.MPU9250 import MPU9250
import numpy as np
from imusensor.filters import kalman
import matplotlib.animation as animation
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d import Axes3D
import math
class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))

        return np.min(zs)


def get_cube(scale,x_offset=0,y_offset=0,z_offset=0):
  phi = np.arange(1,10,2)*np.pi/4
  Phi, Theta = np.meshgrid(phi, phi)
  x = np.cos(Phi)*np.sin(Theta)
  y = np.sin(Phi)*np.sin(Theta)
  z = np.cos(Theta)/np.sqrt(2)
  return x+(x_offset*scale) ,y+(y_offset*scale),z+(z_offset*scale)





class IMU(MPU9250.MPU9250):
   
   def load_config(self,configfile):
      super().loadCalibDataFromFile(configfile)

   def calibrate(self):
      super().caliberateAccelerometer()
      super().caliberateMagPrecise()
      
   def update(self):
      super().readSensor()
      super().computeOrientation()
      
   def status(self):
      print ("Accel x: {0} ; Accel y : {1} ; Accel z : {2}".format(self.AccelVals[0], self.AccelVals[1], self.AccelVals[2]))
      print ("Gyro x: {0} ; Gyro y : {1} ; Gyro z : {2}".format(self.GyroVals[0], self.GyroVals[1], self.GyroVals[2]))
      print ("Mag x: {0} ; Mag y : {1} ; Mag z : {2}".format(self.MagVals[0], self.MagVals[1], self.MagVals[2]))
      
      print("roll: {0} ; pitch : {1} ; yaw : {2}".format(super().roll, super().pitch, super().yaw))
      
address = 0x68
bus = smbus.SMBus(1)
imu = IMU(bus,address)
imu.begin()
imu.setAccelRange("AccelRangeSelect2G")
imu.setGyroRange("GyroRangeSelect250DPS")
# imu.setLowPassFilterFrequency(AccelLowPassFilter184)
# imu.calibrate()
# imu = MPU9250.MPU9250(bus, address)
# imu.begin()
imuFilter = kalman.Kalman()
imu.update()
imuFilter.roll = imu.roll
imuFilter.pitch = imu.pitch
imuFilter.yaw = imu.yaw
startTime = time.time()
currTime = startTime
count = 0

rawRoll = []
rawPitch = []
rawYaw = []
kalRoll = []
kalPitch = []
kalYaw = []
timeList = []
while True:
   # imu.readSensor()
   # imu.computeOrientation()
   # print("roll: {0} ; pitch : {1} ; yaw : {2}".format(imu.roll, imu.pitch, imu.yaw))
   imu.update()
   newTime = time.time()
   dt = newTime - currTime
   currTime = newTime
   
   imuFilter.computeAndUpdateRollPitchYaw(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2], imu.GyroVals[0], imu.GyroVals[1], imu.GyroVals[2],\
												imu.MagVals[0], imu.MagVals[1], imu.MagVals[2], dt)
   print('raw values')
   imu.status()
   rawRoll.append(imu.roll)
   rawPitch.append(imu.pitch)
   rawYaw.append(imu.yaw)
   print('filtered')
   print("Kalmanroll:{0} KalmanPitch:{1} KalmanYaw:{2} ".format(imuFilter.roll, imuFilter.pitch, imuFilter.yaw))
   kalRoll.append(imuFilter.roll)
   kalPitch.append(imuFilter.pitch)
   kalYaw.append(imuFilter.yaw)
   count += 1
   totTime = currTime - startTime
   print('time:',totTime)
   timeList.append(totTime)
   print('frame count: ' , count)
   
   if totTime >= 1:
      break
   
   time.sleep(0.01)
   
# fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2)
# ax1.plot(timeList, rawRoll, color="orange")
# ax2.plot(timeList, kalRoll, color="orange",linestyle='dashed')
# ax3.plot(timeList, rawPitch, color="green")
# ax4.plot(timeList, kalPitch, color="green",linestyle='dashed')
# ax5.plot(timeList, rawYaw, color="blue")
# ax6.plot(timeList, kalYaw, color="blue",linestyle='dashed')

fig, (ax1, ax2, ax3) = plt.subplots(3)
ax1.set_ylabel('Roll')
ax1.plot(timeList, rawRoll, color="orange")
ax1.plot(timeList, kalRoll, color="orange",linestyle='dashed')
ax2.set_ylabel('Pitch')
ax2.plot(timeList, rawPitch, color="green")
ax2.plot(timeList, kalPitch, color="green",linestyle='dashed')
ax3.set_ylabel('Yaw')
ax3.plot(timeList, rawYaw, color="blue")
ax3.plot(timeList, kalYaw, color="blue",linestyle='dashed')

fig.text(0.5, 0.04, 'time', ha='center', va='center')
# fig.text(0.06, 0.5, 'yaw roll pitch', ha='center', va='center', rotation='vertical')

# plt.xlabel("time")
# plt.ylabel("pitch roll yaw")
# plt.title('imu plots')
plt.savefig('imu_data.png')

plt.clf()

# define cube vertices
vertices = np.array([[-1, -1, -1],
                     [1, -1, -1],
                     [1, 1, -1],
                     [-1, 1, -1],
                     [-1, -1, 1],
                     [1, -1, 1],
                     [1, 1, 1],
                     [-1, 1, 1]])

# define edges joining the vertices
edges = [(0, 1), (1, 2), (2, 3), (3, 0),
         (4, 5), (5, 6), (6, 7), (7, 4),
         (0, 4), (1, 5), (2, 6), (3, 7)]

# define the plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# set plot limits
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])

# define the animation function
def rotate(i):
    ax.clear()
    # rotate the vertices around the x and y axes
   #  c, s = np.cos(angle), np.sin(angle)
    
    xc,xs = np.cos(math.radians(kalRoll[i])) , np.sin(math.radians(kalRoll[i]))
    yc,ys = np.cos(math.radians(kalPitch[i])) , np.sin(math.radians(kalPitch[i]))
    zc,zs = np.cos(math.radians(kalYaw[i])) , np.sin(math.radians(kalYaw[i]))
   
    rotx = np.array([[1, 0, 0],
                     [0, xc, -xs],
                     [0, xs, xc]])
    
    roty = np.array([[yc, 0, ys],
                     [0, 1, 0],
                     [-ys, 0, yc]])
    
    
    rotz = np.array([[zc, -zs, 0],
                     [zs, zc, 0],
                     [0, 0, 1]])
   #                                     (ry * (rx * v.T)).T
    vertices_rot = np.dot(rotz,np.dot(roty, np.dot(rotx, vertices.T))).T
    # plot the rotated cube
    for edge in edges:
        ax.plot3D(vertices_rot[edge, 0], vertices_rot[edge, 1], vertices_rot[edge, 2], 'blue')


print(len(timeList))

# create the animation object
anim = animation.FuncAnimation(fig, rotate, frames=len(timeList), interval=len(timeList))

#np.linspace(0, 2*np.pi, 50)

anim.save(filename="imu_3d_orientation.mp4", writer="ffmpeg")




# fig = plt.figure(figsize=(5, 5))
# ax = fig.add_subplot(111, projection='3d')




# cube_s = 0.5

# x,y,z = get_cube(1/cube_s,x_offset=0.0,y_offset=0.0 ,z_offset=0.0)
# print(x)
# print(y)
# print(z)
# ax.plot_surface(x*cube_s, y*cube_s, z*cube_s,alpha=0.3)








# ax.set_xlim([-1.0, 1.0])
# ax.set_ylim([-1.0, 1.0])
# ax.set_zlim([-1, 1])
# ax.set_xlabel('$X$', fontsize=40, rotation=150)
# ax.set_ylabel('$Y$', fontsize=40)
# ax.set_zlabel('$z$', fontsize=40, rotation=60)
# ax.view_init(azim=-65, elev=15,roll=0)
# plt.savefig('imu_3d_orientation.png')