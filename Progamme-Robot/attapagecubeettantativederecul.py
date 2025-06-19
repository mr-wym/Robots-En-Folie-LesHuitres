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
VITESSE_LENTE = 170
VITESSE_RECULE = 130
NB_LEDS = 8
pinceValue = True
vitesseRobot = 0
statusDeplacement = "AVANCE"
statusLigne = 1
compteurLigne = 0
cubeARecup = []
dist = 0 


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
      duty = int((70 / 180) * 102 + 26)
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

# def set_moteur(a1, a2, b1, b2):
#     set_pwm(moteurs['A1'], a1)
#     set_pwm(moteurs['A2'], a2)
#     set_pwm(moteurs['B1'], b1)
#     set_pwm(moteurs['B2'], b2)

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

def recule(vitesse):
    # set_moteur(vitesse, 0, vitesse, 0)
    set_pwm(IN1, 0)
    set_pwm(IN2, vitesse)
    set_pwm(IN3, 0)
    set_pwm(IN4, vitesse)

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

def droite90():
    print("droite90")
    set_pwm(IN1, 255)
    set_pwm(IN2, 0)
    set_pwm(IN3, 0)
    set_pwm(IN4, 255)
    time.sleep(0.35)

vitesseFindCube = 130
def droite10():
    print("droite10")
    set_pwm(IN1, vitesseFindCube)
    set_pwm(IN2, 0)
    set_pwm(IN3, 0)
    set_pwm(IN4, vitesseFindCube)
    # time.sleep(0.35)
    
def gauche90(): 
    print("gauche90")
    set_pwm(IN1, 0)
    set_pwm(IN2, 170)
    set_pwm(IN3, 210)
    set_pwm(IN4, 0)
    time.sleep(0.35)
    stop()


def getMission():
    try:
        reponse = urequests.get(f"http://{IpNous}/instructions?robot_id={UUID}")
        texte_json = reponse.text
        donnees = json.loads(texte_json)
        cubeARecup = donnees.get("rows", [])
        print("cube à récupérer" , cubeARecup)
    except Exception as e:
        print("Erreur de requête :", e)

def postTelemetry(vitesseRobot, dist, statusDeplacement, statusLigne, pinceValue, UUID):
    payload = {
        "vitesse": vitesseRobot,
        "distance_ultrasons": dist,
        "status_deplacement": statusDeplacement,
        "ligne": statusLigne,
        "status_pince": pinceValue,
        "robot_id": UUID
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

def getCubee() :
    global dist
    print("getCube")
    
    dist = mesure_distance()
    
    if dist < 0:
      dist = 40
    print("dzaighezqliughvte", dist)
    
    while dist > 5.0:
    #   print("dans le whielelzfjzirgozvr")
      avance(150)
      dist = mesure_distance()
      if dist < 0:
        dist = 40
      print("ditancee", dist)
    if 0 <= dist <= 5:
        print("dans le iffff")
        stop()
        time.sleep(5)
        # if not pinceValue:
        pinceValue = False
        pince(pinceValue)
        time.sleep(30)
     # else:
      #    suivre_ligne()
       #   if pinceValue:
        #      pinceValue = False
         #     pince(pinceValue)
  
def returnPiste():
    g, d = capteur_gauche.value(), capteur_droite.value()
    
    while g and d:
        print("recule")
        recule(120)
        
    
    
    
def getCube():
    global dist, pinceValue
    print("getCube")

    # Première mesure
    dist = mesure_distance()
    if dist < 0:
        dist = 40  # Valeur par défaut en cas d'erreur
    print("Distance initiale:", dist)

    # Avancer jusqu'à ce que la distance soit inférieure à 4 cm
    while dist > 3.0:
        avance(120)
        time.sleep(0.05)
        dist = mesure_distance()
        if dist < 0:
            dist = 40  # Réinitialiser si mesure incorrecte
        print("Distance mesurée:", dist)

    # Une fois proche du cube (< 4 cm), arrêter et fermer la pince
    stop()
    print("stop")
    time.sleep(3)
    print("Cube atteint, arrêt et fermeture de la pince")
    print("pince fermée")
    
    pince(True)
    time.sleep(2)
    print("après sleep")
    returnPiste()
    

def findCube():
  global dist, pinceValue
  dist = mesure_distance()
  print("findCube")
  
  print("dist before = ",dist)
  if dist < 0:
      dist = 40
  print("dist = ",dist)
      
    #   while 0 <= dist >= 30: 
  while dist > 30:
    #   if dist >= 0 and dist <= 30
    print("distance while =", dist)

    # if dist < 0:
    #     print("Erreur de mesure, nouvelle tentative...")
    #     dist = mesure_distance()
    #     continue

    droite10()
    time.sleep(0.08)
    stop()
    time.sleep(0.1)
    dist = mesure_distance()
    if dist < 0:
      dist = 40
    print("distance après mise a jour", dist)
    # time.sleep(2)
    
    # # if 0 < dist <= 30:
    # if dist >= 0 and dist <= 30:
    #     print("Cube détecté à", dist, "cm")
    #     getCube()
    #     break
  if 0 <= dist <= 25:
        print("Cube détecté à", dist, "cm")
        stop()
        for i in range(3):
            print("la")
            droite10()
            time.sleep(0.1)
            stop()
            time.sleep(0.4)
        
        time.sleep(2)
        getCube()
 
      
#   time.sleep(10)
#   global compteurLigne
#   #if compteurLigne = 2 | compteurLigne = 3 | compteurLigne = 7 | compteurLigne =10 :
#   if compteurLigne in cubeARecup:
#     print("dans le if compteur ligne dans le liste")
#     droite90()
#     stop()
    
#     time.sleep(10)
    
#     # gauche90()
#     # time.sleep(2)
#     # getCube()
#     stop()

#  Suivi de ligne 
def suivre_ligne():#****************************************************
    global compteurLigne
    g, d = capteur_gauche.value(), capteur_droite.value()
    # print(capteur_droite.value())
  
    # if g and d and compteurLigne <= 10:
    if g and d:
        
        # print("compteur before", compteurLigne)
        # compteurLigne += 1 
        # print("compteur after", compteurLigne)
        set_led_color(0, 255, 255,255)
        # recule(MAX_VITESSE)
        stop()
        time.sleep(0.5)
        # avance(MAX_VITESSE)
        # while g and d:
        findCube()
      
    elif d:
        stop()
        time.sleep(0)
        droite(VITESSE_LENTE)
        # print("Droite")
        set_led_color(2, 255, 128, 0)
    elif g:
        stop()
        time.sleep(0)
        gauche(VITESSE_LENTE)
        # print("Gauche")
        set_led_color(1, 255, 128, 0)
    else:
        avance(MAX_VITESSE)
        # print("Avance")
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
    # droite90()
    # time.sleep(2)
    # gauche90()
    # time.sleep(2)
    
    pince(False)
    time.sleep(0.5)
    # if connect_wifi() == True:
        #print("ici")
        # getMission()
        
    clignoter_leds(255, 0, 0, 0.2)

    #set_led_color(0, 255, 255, 255)

firststart = 0
if firststart == 0:
    firststart = 1
    start()
    
#  Boucle principale 
while True:
    #while True:   
    #dist = mesure_distance()
    #postTelemetry(vitesseRobot, dist, statusDeplacement, statusLigne, pinceValue, UUID)
    #time.sleep(1)
    suivre_ligne()

    time.sleep(0.05)  # plus réactif, sans surcharge