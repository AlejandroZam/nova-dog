import pygame
from pygame import joystick
pygame.init()
pygame.joystick.init()


num_joysticks = joystick.get_count()

if num_joysticks > 0:
    controller = joystick.Joystick(0)
    controller.init()
    print("Controller connected:", controller.get_name())
else:
    print("No controller detected.")
    
num_axes = controller.get_numaxes()
num_buttons = controller.get_numbuttons()
num_hats = controller.get_numhats()

print('num of axes ', num_axes)
print('num of buttons ', num_buttons)
print('num of hats ', num_hats)
joysticks = {}
done = False

while not done:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         done = True   
      if event.type == pygame.JOYBUTTONUP:
         print("Joystick button released.")
      if event.type == pygame.JOYDEVICEADDED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks[joy.get_instance_id()] = joy
            print(f"Joystick {joy.get_instance_id()} connencted")

      if event.type == pygame.JOYDEVICEREMOVED:
            del joysticks[event.instance_id]
            print(f"Joystick {event.instance_id} disconnected")
            done=True
         
         
pygame.quit()