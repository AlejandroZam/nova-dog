import json


# Addresses
# imu 0x50
# oled 0x3C
# servo controller 0x40
# sensor 0x29

class IMU:
    name='_imu_'
    def __init__(self,order,rate):
        self.order = order
        self.rate = rate
        print('init')
    def update(self):
        print('update')
    def updatederivative(self):
        print('updatederivative')
    def set_name(self,name):
        self.name = name
        
class LEGS:
    name='_legs_'
    def __init__(self,order,rate):
        self.order = order
        self.rate = rate
        print('init')
    def update(self):
        print('update')
    def updatederivative(self):
        print('updatederivative')
    def set_name(self,name):
        self.name = name
        
class CAM:
    name='_cam_'
    def __init__(self,order,rate):
        self.order = order
        self.rate = rate
        print('init')
    def update(self):
        print('update')
    def updatederivative(self):
        print('updatederivative')
    def set_name(self,name):
        self.name = name
        
class SENSOR:
    name='_sensor_'
    def __init__(self,order,rate):
        self.order = order
        self.rate = rate
        print('init')
    def update(self):
        print('update')
    def updatederivative(self):
        print('updatederivative')
    def set_name(self,name):
        self.name = name
        
class OLED:
    name='_oled_'
    def __init__(self,order,rate):
        self.order = order
        self.rate = rate
        print('init')
    def update(self):
        print('update')
    def set_name(self,name):
        self.name = name
        
class USERINTERFACE:
    def __init__(self,order,rate):
        self.order = order
        self.rate = rate
        print('init')
    def update(self):
        print('update')
    def set_name(self,name):
        self.name = name


class ROBOT:
    
    bot_status = ['initializing', 'moving', 'error', 'idle','thinking','finding']

    modules = {}
    updatelist = []
    updatederivative = []
    
    alive = True
    status = bot_status[3]
    def __init__(self):

        self.modules['imu'] = IMU(1,200)
        self.modules['legs'] = LEGS(2,60)
        self.modules['front_cam'] = CAM(3,30)
        self.modules['voltagesensor'] = SENSOR(4,3)
        self.modules['tof_1'] = SENSOR(5,5)
        self.modules['tof_2'] = SENSOR(6,5)
        self.modules['tof_3'] = SENSOR(7,5)
        self.modules['tof_4'] = SENSOR(8,5)
        self.modules['tof_5'] = SENSOR(9,5)
        self.modules['xbox_input'] = USERINTERFACE(10,10)

        for k,v in self.modules.items():
            print(k)

        
    def init_params(self):
        print('update')
    
    def update(self):
        for k,v in self.modules.items():
            print(k)
        print('update')
        
    def updatederivative(self):
        for k,v in self.modules.items():
            print(k)
        print('updatederivative')
        
def main():

    #init here
    dog = ROBOT()
    
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




