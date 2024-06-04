import json
import sched, time

# Addresses
# imu 0x50
# oled 0x3C
# servo controller 0x40
# sensor 0x29


# class COMPONENTS:
#     def __init__(self,order,rate,starttime,duration=1):
#         self.order = order
#         self.rate = 1/rate
#         print('init')
#     def update(self):
#         print(' update ',self.count)
#     def updatederivative(self):
#         print('updatederivative')
#     def set_name(self,name):
#         self.name = name
        

class IMU:
    id=0
    name='_imu_'
    count = 0
    def __init__(self):
        print(self.name+'::init')
        
        
    def update(self):
        self.count += 1
        print(self.name+'::update ',self.count)
        
    def updatederivative(self):
        print(self.name+'::updatederivative')
    def set_name(self,name):
        self.name = name
        
class LEGS:
    id=0
    name='_legs_'
    count = 0
    def __init__(self):
        print(self.name+'::init')
        
        
    def update(self):
        self.count += 1
        print(self.name+'::update ',self.count)
        
    def updatederivative(self):
        print(self.name+'::updatederivative')
    def set_name(self,name):
        self.name = name
        
class CAM:
    id=0
    name='_cam_'
    count = 0
    def __init__(self):
        print(self.name+'::init')
        
        
    def update(self):
        self.count += 1
        print(self.name+'::update ',self.count)
        
    def updatederivative(self):
        print(self.name+'::updatederivative')
    def set_name(self,name):
        self.name = name
        
class SENSOR:
    id=0
    name='_sensor_'
    count = 0
    def __init__(self):
        print(self.name+'::init')
        
    def update(self):
        self.count += 1
        print(self.name+'::update ',self.count)
        
    def updatederivative(self):
        print(self.name+'::updatederivative')
    def set_name(self,name):
        self.name = name
        
class OLED:
    id=0
    name='_oled_'
    count = 0
    def __init__(self):
        print(self.name+'::init')
        
        
    def update(self):
        self.count += 1
        print(self.name+'::update ',self.count)
            
    def set_name(self,name):
        self.name = name
        
class USERINTERFACE:
    id=0
    name='_input_'
    count = 0
    def __init__(self):
        print(self.name+'::init')
        
    def update(self):
        self.count += 1
        print(self.name+'::update ',self.count)
  
        
    def set_name(self,name):
        self.name = name


class ROBOT:
    
    bot_status = ['initializing', 'moving', 'error', 'idle','thinking','finding']

    modules = {}
    updatelist = []
    updatederivative = []

    alive = True
    status = bot_status[3]
    def __init__(self,):
        
        self.count = 0
        self.duration = 1
        
        self.starttime = time.time()
        
        self.endtime = self.starttime + self.duration
        
        self.modules['imu'] = IMU()
        self.modules['legs'] = LEGS()
        self.modules['front_cam'] = CAM()
        self.modules['voltagesensor'] = SENSOR()
        self.modules['tof_1'] = SENSOR()
        self.modules['tof_2'] = SENSOR()
        self.modules['tof_3'] = SENSOR()
        self.modules['tof_4'] = SENSOR()
        self.modules['tof_5'] = SENSOR()
        self.modules['xbox_input'] = USERINTERFACE()
 

        for k,v in self.modules.items():
            v.set_name(k)
        
    
    def init_params(self):
        print('read init params')
    
    def update(self):
        self.count += 1
        print('dog::update ',self.count)

        for k,v in self.modules.items():
            v.update()
        
        
    def updatederivative(self):

        print('updatederivative')
        
def main():
    global scheduler
    scheduler = sched.scheduler(time.time, time.sleep)
    #init here
    dog = ROBOT()

    duration = 1
    starttime = time.time()
    endtime = starttime + duration


    while(time.time()<=endtime):
        dog.update()
    
    # run here
    
    # try: 
    #     while dog.alive:
    #         print(dog.status)
            
    # except KeyboardInterrupt:
    #     print('kill dog')
    #     dog.alive = False





if __name__ == "__main__":
    main()




