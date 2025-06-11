from machine import Pin, PWM
import time

# Configuration du servomoteur
servo = PWM(Pin(15), freq=50)

def set_angle(angle):
    duty = int((angle / 180) * 102 + 26)
    print(f"Réglage de l'angle à {angle}°, valeur PWM : {duty}")
    servo.duty(duty)

# Configuration du capteur ultrason (Trig sur D13, Echo sur D14 par exemple)
trig = Pin(13, Pin.OUT)
echo = Pin(14, Pin.IN)

def mesure_distance():
    # Envoi d'une impulsion sur Trig
    trig.off()
    time.sleep_us(2)
    trig.on()
    time.sleep_us(10)
    trig.off()
    
    # Mesure de la durée de l'écho
    while echo.value() == 0:
        start = time.ticks_us()
    while echo.value() == 1:
        end = time.ticks_us()
    
    duration = time.ticks_diff(end, start)
    distance_cm = duration / 58.0  # Conversion en cm
    print(f"Distance mesurée : {distance_cm:.2f} cm")
    return distance_cm

print("Démarrage du programme de contrôle du servomoteur et mesure de distance.")

while True:
    distance = mesure_distance()
    
    print("Pince fermée")
    set_angle(60)
    time.sleep(3)
    
    distance = mesure_distance()
    
    print("Pince ouverte")
    set_angle(0)
    time.sleep(3)
