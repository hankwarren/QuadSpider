# connect with browser: http://<address>
# The address should be on the display

import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C


from pca9685 import PCA9685
# from picocat import Servos
from servo import Servos

sda = Pin(14)
scl = Pin(15)
id = 1
i2c1 = I2C(id=id, sda=sda, scl=scl)

pca = PCA9685(i2c=i2c1)
# pca.i2c = i2c
servo = Servos(i2c=i2c1)

WIDTH = 128
HEIGHT = 32

i2c0 = I2C(0, scl = Pin(17), sda = Pin(16), freq = 200000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c0)


ssid = 'Frontier6560'
password = '9578089842'

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    print(wlan.ifconfig())
    return ip

def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(temperature, state):
    html = f"""
<!DOCTYPE html>
<html>
<body>
<form action="./lighton">
<input type="submit" value="Light on" />
</form>
<form action="./lightoff">
<input type="submit" value="Light off" />
</form>
<p>LED is {state}</p>
<p>Temperature is {temperature}</p>
</body>
</html>
"""
    return str(html)

def serve(connection):
    state = 'OFF'
    pico_led.off()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print('------------------------')
        print(request)
        
        try:
            request = request.split()[1]
            print(request)
        except IndexError:
            pass
        if request == '/lighton?':
            pico_led.on()
            state = 'ON'
            for a in range(0, 180, 10):
                servo.position(index=0, degrees=a)
                sleep(0.1)
            for a in range(180, 0, -10):
                servo.position(0, degrees=a)
                sleep(0.1)

        elif request == '/lightoff?':
            pico_led.off()
            state = 'OFF'
            for a in range(0, 180, 10):
                servo.position(index=4, degrees=a)
                sleep(0.1)
            for a in range(180, 0, -10):
                servo.position(4, degrees=a)
                sleep(0.1)

        temperature = pico_temp_sensor.temp
        
        html = webpage(temperature, state)
        client.send(html)
        client.close()
        oled.fill(0)
        oled.text("Hello World", 0, 0)
        oled.text(str(ip), 0, 12)
        oled.text(state, 0, 24)
        oled.show()


try:
    ip = connect()
    oled.fill(0)
    oled.text(str(ip), 0, 12)
    oled.show()

    connection = open_socket(ip)
    serve(connection)
    
except KeyboardInterrupt:
    machine.reset()
    
    
    

