from machine import Pin, time_pulse_us
import time

trig = Pin(25, Pin.OUT)
echo = Pin(33, Pin.IN)

def mesure_distance():
    trig.value(0)
    time.sleep_us(2)

    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    try:
        duration = time_pulse_us(echo, 1, 30000)
    except OSError as e:
        print(e)
        return None

    distance = (duration / 2) / 29.1
    return round(distance, 2)

while True:
    dist = mesure_distance()
    if dist is not None:
        print(dist)

    time.sleep(1)
