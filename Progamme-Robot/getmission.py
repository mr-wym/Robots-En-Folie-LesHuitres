from machine import Pin, PWM, time_pulse_us
import time
import neopixel
import network
import network
import time
import urequests
import json

#  Constantes 
UUID = '53d67923-704f-4b97-b6d4-64a0a04ca5de'
PWM_FREQ = 1000
MAX_DUTY = 1023
MAX_VITESSE = 150
VITESSE_LENTE = 210
VITESSE_RECULE = 170
NB_LEDS = 8
pinceValue = True
vitesse = 0
statusDeplacement = "AVANCE"
statusLigne = 1

IpNous = '10.7.5.42:8000'
IPMax = '10.7.5.42:8000'
IpGhost = '10.7.5.42:8000'
IpPath = '10.7.5.42:8000'
IpOsr = '10.7.5.182:8000'
IpPasta = '10.7.5.42:8000'

SSID = 'IMERIR Fablab'
PASSWORD = 'imerir66'

urlInstrcutions = f'http://{IpNous}/instructions'
urlTelemetry = f'http://{IpNous}/telemetry'

# #  Initialisation des moteurs 
# moteurs = {
#     'A1': PWM(Pin(18), freq=PWM_FREQ),
#     'A2': PWM(Pin(19), freq=PWM_FREQ),
#     'B1': PWM(Pin(21), freq=PWM_FREQ),
#     'B2': PWM(Pin(22), freq=PWM_FREQ),
# }

IN1 = PWM(Pin(18), freq=PWM_FREQ)
IN2 = PWM(Pin(19), freq=PWM_FREQ)
IN3 = PWM(Pin(21), freq=PWM_FREQ)
IN4 = PWM(Pin(22), freq=PWM_FREQ)

# Initialisation de l'utrason *
trig = Pin(25, Pin.OUT)
echo = Pin(33, Pin.IN)

# Initialisation Servomoteur *
servo = PWM(Pin(15), freq=50)

#  Initialisation des LEDs 
np1 = neopixel.NeoPixel(Pin(12), NB_LEDS)
np2 = neopixel.NeoPixel(Pin(2), NB_LEDS)

#  Capteurs de statusLigne 
capteur_gauche = Pin(26, Pin.IN)
capteur_droite = Pin(27, Pin.IN)


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

def clignoter_leds(r, g, b, nb_fois, delai=0.3):
    for _ in range(nb_fois):
        set_led_color(0, r, g, b)
        time.sleep(delai)
        set_led_color(0, 0, 0, 0)
        time.sleep(delai)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    time.sleep(1)
    wlan.active(True)
    #  wlan.connect(SSID, PASSWORD)
    print("Connexion au Wi-Fi...")
    
    if not wlan.isconnected():
        try:
            wlan.connect(SSID, PASSWORD)
        except OSError as e:
            print("Erreur lors de la tentative de connexion :", e)
            clignoter_leds(255, 0, 0, 3)
          
            return False
    else:
      clignoter_leds(0, 255, 0, 3, 0.2)

    for _ in range(20):  # max 10s d’attente
        clignoter_leds(0, 0, 255, 1, 0.2)
        if wlan.isconnected():
            print("Connecté, IP :", wlan.ifconfig()[0])
            clignoter_leds(0, 255, 0, 3, 0.5)
            return True
        time.sleep(0.5)

    print(" Échec de la connexion Wi-Fi.")
    return None

def pince(openClose):
    print(openClose)
    if openClose == True:
      print("dans true")
      duty = int((60 / 180) * 102 + 26)
      servo.duty(duty)
    elif openClose == False:
      print("dans false")
      duty = int((0 / 180) * 102 + 26)
      print(duty)
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

#  Commandes de mouvement 
def stop():
    # set_moteur(0, 0, 0, 0)
    set_pwm(IN1, 0)
    set_pwm(IN2, 0)
    set_pwm(IN3, 0)
    set_pwm(IN4, 0)

def avance(vitesse):
    # set_moteur(vitesse, 0, vitesse, 0)
    set_pwm(IN1, vitesse)
    set_pwm(IN2, 0)
    set_pwm(IN3, vitesse)
    set_pwm(IN4, 0)

def droite(vitesse):
    # set_moteur(vitesse, 0, 0, VITESSE_RECULE)
    set_pwm(IN1, vitesse)
    set_pwm(IN2, 0)
    set_pwm(IN3, 0)
    set_pwm(IN4, VITESSE_RECULE)

def gauche(vitesse):
    # set_moteur(0, VITESSE_RECULE, vitesse, 0)
    set_pwm(IN1, 0)
    set_pwm(IN2, VITESSE_RECULE)
    set_pwm(IN3, vitesse)
    set_pwm(IN4, 0)

def getMission():
    try:
        reponse = urequests.get(f"http://{IpNous}/instructions?robot_id={UUID}")
        print("Code HTTP :", reponse.status_code)
        print("Réponse :")
        print(reponse.text)
        reponse.close()
    except Exception as e:
        print("Erreur de requête :", e)

def postTelemetry(vitesse, dist, statusDeplacement, statusLigne, pinceValue, UUID):
    payload = {
        "vitesse": vitesse,
        "dist": dist,
        "statusDeplacement": statusDeplacement,
        "statusLigne": statusLigne,
        "pinceValue": pinceValue,
        "uuidNous": UUID
    }
    print(payload)
    try:
        reponse = urequests.post(
            urlTelemetry,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        print("Code réponse:", reponse.status_code)
        print("Réponse serveur:", reponse.text)
        reponse.close()
    except Exception as e:
        print("Erreur lors de l'envoi de la télémétrie:", e)
        
        
    #     f"http://{IpNous}/telemetry,?robot_id={UUID}")
    #     print("Code HTTP :", reponse.status_code)
    #     print("Réponse :")
    #     print(reponse.text)
    #     reponse.close()
    # except Exception as e:
    #     print("Erreur de requête :", e)

      
#  Suivi de ligne 
def suivre_ligne():#****************************************************
    g, d = capteur_gauche.value(), capteur_droite.value()
    print(capteur_droite.value())
    #if g and d:
        #set_led_color(0, 255, 0, 0)
        #avance(MAX_VITESSE)
        #print("Avance")
      
    if d:
        stop()
        time.sleep(0)
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
        set_led_color(0, 0, 0, 0)
    #stop()


def mesure_distance():#*
    trig.value(0)
    time.sleep_us(5)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    try:
        duration = time_pulse_us(echo, 1, 10000)
        distance = (duration / 2) / 29.1
        return round(distance, 2)
    except OSError:
      return -1

    test = getMission()
    print(test)


def start():
    if connect_wifi() == True:
        print("ici")
        getMission()

    #set_led_color(0, 255, 255, 255)
    pince(pinceValue)

start()
  
    
#  Boucle principale 
while True:
    #while True:   
  
    postTelemetry(vitesse, dist, statusDeplacement, statusLigne, pinceValue, UUID)
    time.sleep(1)

    dist = mesure_distance()

    if 0.03 <= dist <= 5.0:
        stop()
        if not pinceValue:
            pinceValue = True
            pince(pinceValue)
    else:
        #suivre_ligne()
        if pinceValue:
            pinceValue = False
            pince(pinceValue)

    time.sleep(0.05)  # plus réactif, sans surcharge