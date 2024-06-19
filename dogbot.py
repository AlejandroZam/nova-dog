import json
import sched, time
import threading
from wt901.imu import WT901

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
    def __init__(self,order,rate,starttime,duration=1):
        self.order = order
        self.rate = 1/rate
        self.duration = duration
        self.starttime = starttime
        self.endtime = starttime + duration
        print(self.name+'::init')
        
    def update(self,curtime):
        self.count += 1
        print(self.name+':: update ',self.count)

        if self.endtime <= curtime:
            try:
                scheduler_1.cancel(self.id)
                return
            except:
                return
        else:
            self.id = scheduler_1.enter(self.rate,self.order,self.update,(time.time(),))
        
    def updatederivative(self):
        print(self.name+'::updatederivative')
    def set_name(self,name):
        self.name = name
        
class LEGS:
    id=0
    name='_legs_'
    count = 0
    def __init__(self,order,rate,starttime,duration=1):
        self.order = order
        self.rate = 1/rate
        self.duration = duration
        self.starttime = starttime
        self.endtime = starttime + duration
        print(self.name+'::init')
        
    def update(self,curtime):
        print(self.name+':: update ',self.count)
        self.count += 1
        if self.endtime <= curtime:
            try:
                scheduler_1.cancel(self.id)
                return
            except:
                return
        else:
            self.id = scheduler_1.enter(self.rate,self.order,self.update,(time.time(),))
        
    def updatederivative(self):
        print(self.name+'::updatederivative')
    def set_name(self,name):
        self.name = name
        
class CAM:
    id=0
    name='_cam_'
    count = 0
    def __init__(self,order,rate,starttime,duration=1):
        self.order = order
        self.rate = 1/rate
        self.duration = duration
        self.starttime = starttime
        self.endtime = starttime + duration
        print(self.name+'::init')
        
    def update(self,curtime):
        self.count += 1
        print(self.name+':: update ',self.count)
        
        if self.endtime <= curtime:
            try:
                scheduler_2.cancel(self.id)
                return
            except:
                return
        else:
            self.id = scheduler_2.enter(self.rate,self.order,self.update,(time.time(),))
        
    def updatederivative(self):
        print(self.name+'::updatederivative')
    def set_name(self,name):
        self.name = name
        
class SENSOR:
    id=0
    name='_sensor_'
    count = 0
    def __init__(self,order,rate,starttime,duration=1):
        self.order = order
        self.rate = 1/rate
        self.duration = duration
        self.starttime = starttime
        self.endtime = starttime + duration
        print(self.name+'::init')
    def update(self,curtime):
        self.count += 1
        print(self.name+':: update ',self.count)
        if self.endtime <= curtime:
            try:
                scheduler_1.cancel(self.id)
                return
            except:
                return
        else:
            self.id = scheduler_1.enter(self.rate,self.order,self.update,(time.time(),))
        
        
    def updatederivative(self):
        print(self.name+'::updatederivative')
    def set_name(self,name):
        self.name = name
        
class OLED:
    id=0
    name='_oled_'
    count = 0
    def __init__(self,order,rate,starttime,duration=1):
        self.order = order
        self.rate = 1/rate
        self.duration = duration
        self.starttime = starttime
        self.endtime = starttime + duration
        print(self.name+'::init')
        
    def update(self,curtime):
        self.count += 1
        print(self.name+':: update ',self.count)
        if self.endtime <= curtime:
            try:
                scheduler_1.cancel(self.id)
                return
            except:
                return
        else:
            self.id = scheduler_1.enter(self.rate,self.order,self.update,(time.time(),))
            
    def set_name(self,name):
        self.name = name
        
class USERINTERFACE:
    id=0
    name='_input_'
    count = 0
    def __init__(self,order,rate,starttime,duration=1):
        self.order = order
        self.rate = 1/rate
        self.duration = duration
        self.starttime = starttime
        self.endtime = starttime + duration
        print(self.name+'::init')
    def update(self,curtime):
        self.count += 1
        print(self.name+'::update ',self.count)
        if self.endtime <= curtime:
            try:
                scheduler_3.cancel(self.id)
                return
            except:
                return
        else:
            self.id = scheduler_3.enter(self.rate,self.order,self.update,(time.time(),))
        
    def set_name(self,name):
        self.name = name


class ROBOT:
    
    bot_status = ['initializing', 'moving', 'error', 'idle','thinking','finding']
    id=0
    modules = {}
    updatelist = []
    updatederivative = []
    t1 = None
    t2 = None 
    t3 = None
    alive = True
    status = bot_status[3]
    def __init__(self,):
        
        self.rate = 1/400
        self.order = 1
        self.count = 0
        self.duration = 1
        
        self.starttime = time.time()
        
        self.endtime = self.starttime + self.duration
        
        self.modules['imu'] = IMU(2,210,self.starttime)
        self.modules['legs'] = LEGS(3,60,self.starttime)
        self.modules['front_cam'] = CAM(1,30,self.starttime)
        self.modules['voltagesensor'] = SENSOR(5,3,self.starttime)
        self.modules['tof_1'] = SENSOR(6,5,self.starttime)
        self.modules['tof_2'] = SENSOR(7,5,self.starttime)
        self.modules['tof_3'] = SENSOR(8,5,self.starttime)
        self.modules['tof_4'] = SENSOR(9,5,self.starttime)
        self.modules['tof_5'] = SENSOR(10,5,self.starttime)
        self.modules['xbox_input'] = USERINTERFACE(1,10,self.starttime)
 

        
        scheduler_1.enter(self.rate,self.order,self.update,(time.time(),))
        for k,v in self.modules.items():
            v.set_name(k)
            if k == 'xbox_input':
                scheduler_3.enter(v.rate,v.order,v.update,(time.time(),))
            elif k == 'front_cam':
                scheduler_2.enter(v.rate,v.order,v.update,(time.time(),))
            else:
                scheduler_1.enter(v.rate,v.order,v.update,(time.time(),))

        self.t1 = threading.Thread(target=scheduler_1.run, name='t1')
        self.t2 = threading.Thread(target=scheduler_2.run, name='t2')   
        self.t3 = threading.Thread(target=scheduler_3.run, name='t3')  
        # t2 = threading.Thread(target=task2, name='t2')

    
    def run(self):
        # scheduler_1.run()
        self.t1.start()
        self.t2.start()
        self.t3.start()
    
    def init_params(self):
        print('read init params')
    
    def update(self,curtime):
        self.count += 1
        print('dog::update ',self.count)


        if self.endtime <= curtime:
            try:
                scheduler_1.cancel(self.id)
                return
            except:
                return
            









            
        else:
            self.id = scheduler_1.enter(self.rate,self.order,self.update,(time.time(),))
        
        
        
    def updatederivative(self):

        print('updatederivative')
        
def main():
    global scheduler_1
    global scheduler_2
    global scheduler_3
    global scheduler_4
    scheduler_1 = sched.scheduler(time.time, time.sleep)
    scheduler_2 = sched.scheduler(time.time, time.sleep)
    scheduler_3 = sched.scheduler(time.time, time.sleep)
    # scheduler_4 = sched.scheduler(time.time, time.sleep)
    #init here
    dog = ROBOT()
    
    dog.run()
    
    # run here
    
    # try: 
    #     while dog.alive:
    #         print(dog.status)
            
    # except KeyboardInterrupt:
    #     print('kill dog')
    #     dog.alive = False





if __name__ == "__main__":
    main()




