from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
WIDTH = 128
HEIGHT = 32

i2c0 = I2C(0, scl = Pin(17), sda = Pin(16), freq = 200000)
display = SSD1306_I2C(WIDTH, HEIGHT, i2c0)

def update(fill_value, msg1, msg2):
    display.fill(fill_value)
    display.text(str(msg1), 0, 0)
    display.text(str(msg2), 0, 12)
    # oled.text(state, 0, 24)
    display.show()