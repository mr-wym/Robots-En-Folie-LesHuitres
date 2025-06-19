from machine import Pin, PWM
import time
import neopixel

np1 = neopixel.NeoPixel(Pin(12), 8)

np2 = neopixel.NeoPixel(Pin(2), 8)

def set_led_color(r, g, b):
    for i in range(np1.n):
        np1[i] = (r, g, b)
    np1.write()
    
    for i in range(np2.n):
        np2[i] = (r, g, b)
    np2.write()


while True:
    set_led_color(0, 255, 0)
    time.sleep(3)
    
    set_led_color(255, 80, 0)
    time.sleep(3)
