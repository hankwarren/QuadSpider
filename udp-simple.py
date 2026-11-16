# connect with browser: http://<address>
# The address should be on the display

import network
import socket
import ujson

from time import sleep
from picozero import pico_temp_sensor, pico_led
from machine import Pin, I2C

from pca9685 import PCA9685
from servo import Servos
import oled


sda = Pin(14)
scl = Pin(15)
id = 1
i2c1 = I2C(id=id, sda=sda, scl=scl)

#pca = PCA9685(i2c=i2c1)
# pca.i2c = i2c
servo = Servos(i2c=i2c1)


port = 4141

ssid = 'Frontier6560'
password = '9578089842'

def connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    my_ip = wlan.ifconfig()[0]
    print(f'Connected on {my_ip}')
    
#    my_ip = '0.0.0.0'
    return my_ip

def open_socket(ip, port):
    address = (ip, port)
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(address)
    print('bind: ', address)
    return udp_socket

def serve(udp_socket, ip):
    # udp_socket.settimeout(60.0)
    state = 'OFF'
    pico_led.off()
    temperature = 0

    while True:
        # print('recvfrom:')
        
        request = udp_socket.recvfrom(1024)
        
        message = request[0].decode("utf-8")
        address = request[1]
        
        print('------------------------')
        print(message)
        print(address)
        
        json = ujson.loads(message)
        response = "no response"
        
        if json['cmd'] == "servo":
            i = json['servo']
            
            print("servo: ", json['servo'])
            print("angle: ", json['angle'])
            servo.position(index=json['servo'], degrees=json['angle'])
            if i % 2:
                pico_led.on()
            else:
                pico_led.off()
                
            res = "servo: {servo: 2d}, angle: {angle: 2d}"
            response = res.format(servo = json['servo'], angle = json['angle'])
        
        elif json['cmd'] == 'led':
            if json['value'] == 'on':
                pico_led.on()
                response = "led on"
            else:
                pico_led.off()
                response = "led off"
            
            udp_socket.sendto(response, address)
            print("response: ", response)

        oled.update(0, ip, json['cmd'])
        
try:
    ip = connect(ssid, password)
    oled.update(0, ip, "Help")
     
    udp_socket = open_socket(ip, port)
    serve(udp_socket, ip)
    
except KeyboardInterrupt:
    machine.reset()
    