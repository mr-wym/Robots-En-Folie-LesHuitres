from machine import Pin, PWM
import time
import neopixel

#  Constantes 
PWM_FREQ = 1000
MAX_DUTY = 1023
MAX_VITESSE = 150
VITESSE_LENTE = 210
VITESSE_RECULE = 170
NB_LEDS = 8

#  Initialisation des moteurs 
moteurs = {
    'A1': PWM(Pin(18), freq=PWM_FREQ),
    'A2': PWM(Pin(19), freq=PWM_FREQ),
    'B1': PWM(Pin(21), freq=PWM_FREQ),
    'B2': PWM(Pin(22), freq=PWM_FREQ),
}


# Initialisation de l'utrason *
trig = Pin(25, Pin.OUT)
echo = Pin(33, Pin.IN)

# Initialisation Servomoteur *
servo = PWM(Pin(15), freq=50)

#  Initialisation des LEDs 
np1 = neopixel.NeoPixel(Pin(12), NB_LEDS)
np2 = neopixel.NeoPixel(Pin(2), NB_LEDS)

#  Capteurs de ligne 
capteur_gauche = Pin(26, Pin.IN)
capteur_droite = Pin(27, Pin.IN)

pince(True)

def pince(openClose):
    if openClose == True:
      duty = int((60 / 180) * 102 + 26)
    elif openClose == False:
      duty = int((0 / 180) * 102 + 26)
    servo.duty(duty)
  
#  Fonctions utilitaires 
def set_pwm(pwm, value):
    value = max(0, min(value, MAX_VITESSE))
    pwm.duty(int(value * MAX_DUTY / 255))

def set_moteur(a1, a2, b1, b2):
    set_pwm(moteurs['A1'], a1)
    set_pwm(moteurs['A2'], a2)
    set_pwm(moteurs['B1'], b1)
    set_pwm(moteurs['B2'], b2)

def set_led_color(n, r, g, b):
    if n == 1:
      for i in range(NB_LEDS):
        np1[i] = (r, g, b)
        np2[i] = (0, 0, 0)
    elif n == 2:
      for i in range(NB_LEDS):
        np1[i] = (0, 0, 0)
        np2[i] = (r, g, b)
    elif n == 0:
      for i in range(NB_LEDS):
          np1[i] = (r, g, b)
          np2[i] = (r, g, b)
    np1.write()
    np2.write()

#  Commandes de mouvement 
def stop():
    set_moteur(0, 0, 0, 0)

def avance(vitesse):
    set_moteur(vitesse, 0, vitesse, 0)

def droite(vitesse):
    set_moteur(vitesse, 0, 0, VITESSE_RECULE)

def gauche(vitesse):
    set_moteur(0, VITESSE_RECULE, vitesse, 0)
  

#  Suivi de ligne 
def suivre_ligne():
    g, d = capteur_gauche.value(), capteur_droite.value()
    print(capteur_droite.value())
    if g and d:
        set_led_color(0, 255, 0, 0)
        avance(MAX_VITESSE)
        print("Avance")
      
    elif d:
        stop()
        time.sleep(0)  # placeholder si besoin d'un délai
        droite(VITESSE_LENTE)
        print("Droite")
        set_led_color(2, 255, 128, 0)
    elif g:
        stop()
        time.sleep(0)
        gauche(VITESSE_LENTE)
        print("Gauche")
        set_led_color(1, 255, 128, 0)
    else:
        avance(MAX_VITESSE)
        print("Avance")
        set_led_color(0, 0, 0, 255)
    stop()

#  Boucle principale 
while True:
    suivre_ligne()
