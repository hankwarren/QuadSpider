from pca9685 import PCA9685
# from picocat import Servos
from machine import I2C, Pin
from servo import Servos
from ssd1306 import SSD1306_I2C
import time

WIDTH = 128
HEIGHT = 32

sda = Pin(16)
scl = Pin(17)
id = 0
i2c = I2C(id=id, sda=sda, scl=scl)
pca = PCA9685(i2c=i2c)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# pca.i2c = i2c
servo = Servos(i2c=i2c)
iservo = 1

#for s in [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14]:
#    servo.position(index=s, degrees=0)
   #servo.position(index=1, degrees=0)
#    time.sleep(1.0)

#    servo.position(index=s, degrees=90)
    #servo.position(index=1, degrees=90)
#    time.sleep(1.0)
#servo_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
servo_list = [15, 11, 7, 3]

hip_initial = [
    { "servo": 15, "angle": 90 },
    { "servo": 11, "angle": 90 },
    { "servo": 7, "angle": 90 },
    { "servo": 3, "angle": 90 }
]

hip_extend = [
    { "servo": 15, "angle": 0 },
    { "servo": 11, "angle": 180 },
    { "servo": 7, "angle": 180 },
    { "servo": 3, "angle": 0 }
]

knee_initial = [
    { "servo": 14, "angle": 180 },
    { "servo": 10, "angle": 90 },
    { "servo": 6, "angle": 180 },
    { "servo": 2, "angle": 90 }
]

knee_up = [
    { "servo": 14, "angle": 0 },
    { "servo": 10, "angle": 0 },
    { "servo": 6, "angle": 0 },
    { "servo": 2, "angle": 0 }
]
knee_down = [
    { "servo": 14, "angle": 180 },
    { "servo": 10, "angle": 180 },
    { "servo": 6, "angle": 180 },
    { "servo": 2, "angle": 180 }
]

ankle_initial = [
    { "servo": 13, "angle": 90 },
    { "servo": 9, "angle": 90 },
    { "servo": 5, "angle": 90 },
    { "servo": 1, "angle": 90 }    
]
ankle_extend = [
    { "servo": 13, "angle": 0 },
    { "servo": 9, "angle": 0 },
    { "servo": 5, "angle": 0 },
    { "servo": 1, "angle": 0 }    
]


def drive_servos(angle, servo_list):
    for s in servo_list:
        print(f"servo: {s} {angle} degrees")
        servo.position(index=s, degrees=angle)
    time.sleep(1)

def drive_servo_dict(dict_array):
    for s in dict_array:
        print(s)
        print(f'servo: {s["servo"]} angle: {s["angle"]}')
        servo.position(s["servo"], s["angle"])
    time.sleep(2)

#drive_servos(90, servo_list)

oled.fill(0)
oled.hline(0, 0, 127, 1)
oled.text("Hello World", 0, 2)
oled.hline(0, 31, 127, 1)
oled.show()

while True:
    drive_servo_dict(knee_up)
    time.sleep(.1)
    drive_servo_dict(knee_down)
    time.sleep(.1)
    
"""
while True:
    drive_servos(0, servo_list)
    time.sleep(1)
    drive_servos(90, servo_list)
    time.sleep(1)
    drive_servos(180, servo_list)
    time.sleep(1)
    
while True:
    drive_servos(0, servo_list)
    time.sleep(2)
    drive_servos(90, servo_list)
    time.sleep(2)
    drive_servos(180, servo_list)
    time.sleep(2)
    drive_servos(90, servo_list)
    time.sleep(2)
    
for i in range(0, 180, 10):
    print("step:", i)
    drive_servos(0, servo_list)
    time.sleep(0.25)
    drive_servos(90, servo_list)
    time.sleep(0.25)
    drive_servos(180, servo_list)
    time.sleep(0.25)
    drive_servos(90, servo_list)
    time.sleep(.25)
    
for i in range(0,10):
    for a in range(0,180, 10):
        drive_servos(a, servo_list)
        time.sleep(0.1)
    for a in range(180, 0, -10):
        drive_servos(a, servo_list)
        time.sleep(0.1)
    
#servo.position(index=1, degrees=0)
#servo.position(index=2, degrees=0)
#servo.position(index=4, degrees=0)
#servo.position(index=5, degrees=0)
#servo.position(index=6, degrees=0)
"""