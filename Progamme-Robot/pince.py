from machine import Pin, PWM
import time

servo = PWM(Pin(15), freq=50)

def set_angle(angle):
    duty = int((angle / 180) * 102 + 26)
    print(f"{angle} {duty}")
    servo.duty(duty)


while True:
    set_angle(60)
    time.sleep(3)
    
    set_angle(0)
    time.sleep(3)
