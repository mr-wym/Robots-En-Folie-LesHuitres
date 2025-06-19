# Version du 19/06/2025 Team les Huitre
# L'IA generative à aidé dans la rédactions des commentaires 

from machine import Pin, PWM, time_pulse_us
import time
import neopixel
import network
import network
import time
import urequests
import json

#  Variables globales
UUID = '53d67923-704f-4b97-b6d4-64a0a04ca5de' # UUID L'ID du robot 
pwmFrequence = 1000 # Fréquence des moteurs
maxDuty = 1023 # Valeur maximale du duty cycle pour le PWM 
maxVitesse = 150 # Vitesse Max
vitesseLente = 170 # Vitesse Lente
vitesseRecul = 130 # Vitesse de recul
nbLeds = 8 # Nombre de led par bandeau
pinceValue = True # Pince Fermer/Ouverte 
vitesseRobot = 0  # Vitesse du robot 
statusDeplacement = "AVANCE" # Status des déplacements
statusLigne = 1   # Status de la ligne True/false
compteurLigne = 0 # Nombre de check point 
cubeARecup = []   # Liste des cubes à récupère
dist = 0 # Distance

# IP serveur 
IpNous =  '10.7.5.42:8000'  # Les huitres
IPMax =   '10.7.5.148:8000' # Maxence rose
IpGhost = '10.7.5.225:8000'  # Ghosteyes
IpPath =  '10.7.5.119:8000' # Les 3 moutikèire
IpOsr =   '10.7.5.182:8000' # On sais rien (OSR)
IpPasta = '10.7.5.176:8000' # Ctrl C / Ctrl V 

# Connexion WIFI
SSID = 'IMERIR Fablab' # Nom du réseau 
PASSWORD = 'imerir66'  # Mot de passe du Wifi

# URL pour les requêtes HTTP
urlInstrcutions = f'http://{IpNous}/instructions' # URL pour récupérer la mission du robot 
urlTelemetry = f'http://{IpNous}/telemetry' # URL pour poster la telemetrie du robot lors du déplacement
urlSummary = f'http://{IpNous}/summary' # URL pour poster uuid a la fin de la mission


# Initialisation des moteurs 
IN1 = PWM(Pin(18), freq=pwmFrequence) # Pin moteur droite 18
IN2 = PWM(Pin(19), freq=pwmFrequence) # Pin moteur droite 19
IN3 = PWM(Pin(21), freq=pwmFrequence) # Pin moteur gauche 21
IN4 = PWM(Pin(22), freq=pwmFrequence) # Pin moteur gauche 23

# Initialisation de l'utrason
trig = Pin(25, Pin.OUT) # Pin Trig
echo = Pin(33, Pin.IN)  # Pin Echo 

# Initialisation Servomoteur
servo = PWM(Pin(15), freq=50) # Pin servomoteur 15  

# Initialisation des Bandeau LED
np1 = neopixel.NeoPixel(Pin(12), nbLeds) # Pin Bandeau Leds 12 
np2 = neopixel.NeoPixel(Pin(2), nbLeds)  # Pin Bandeau Leds 2

# Capteurs de suivie de ligne  
capteur_gauche = Pin(26, Pin.IN) # Pin Capteur de suivie de ligne  gauche 26
capteur_droite = Pin(27, Pin.IN) # Pin Capteur de suivie de ligne  droite 27

# Fonctions pour les LEDs
def set_led_color(n, r, g, b):
    """!
    Change la couleur des LEDs.
    @param n 0 pour les deux bandeaux, 1 pour le premier, 2 pour le second
    @param r valeur R de la couleur (0-255)
    @param g valeur G de la couleur (0-255)
    @param b valeur B de la couleur (0-255)  
    """
    if n == 1:
      for i in range(nbLeds):
        np1[i] = (r, g, b)
        np2[i] = (0, 0, 0)
    elif n == 2:
      for i in range(nbLeds):
        np1[i] = (0, 0, 0)
        np2[i] = (r, g, b)
    elif n == 0:
      for i in range(nbLeds):
          np1[i] = (r, g, b)
          np2[i] = (r, g, b)
    np1.write()
    np2.write()
    
# Fonction pour faire clignoter les LEDs
def clignoter_leds(r, g, b, nb_fois, delai=0.3):
    """!
    Fait clignoter les LEDs avec la couleur spécifiée.
    @param r valeurs R de la couleur
    @param g valeurs G de la couleur
    @param b valeurs B de la couleur
    @note 0 <= r, g, b <= 255
    @param nb_fois  nombre de clignotements
    @param delai  délai entre les clignotements (en secondes)
    """   
    for _ in range(nb_fois):
        set_led_color(0, r, g, b)
        time.sleep(delai)
        set_led_color(0, 0, 0, 0)
        time.sleep(delai)

# Fonction pour connecter le robot au Wi-Fi
def connect_wifi():
    """!
    Connecte le robot au Wi-Fi.
    @return True si la connexion est réussie, False en cas d'erreur, None si la connexion échoue après 10s
    @note La fonction essaie de se connecter au Wi-Fi avec les SSID et mot de passe définis.
    @return None si la connexion échoue après 10 secondes. 
    """
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

# Fonction pour contrôler la pince
def pince(openClose):
    """!
    Contrôle l'ouverture et la fermeture de la pince.
    @param openClose True pour ouvrir la pince, False pour fermer   
    """
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
    """!
    Définit la valeur du PWM pour un moteur.
    @param pwm l'objet PWM à configurer
    @param value la valeur de vitesse (0-255)   
    """
    value = max(0, min(value, maxVitesse))
    pwm.duty(int(value * maxDuty / 255))

#  Commandes de mouvement 
def stop():
    """!
    Arrête tous les moteurs.
    """
    set_pwm(IN1, 0)
    set_pwm(IN2, 0)
    set_pwm(IN3, 0)
    set_pwm(IN4, 0)
    
    
def avance(vitesse):
    """!
    Avance le robot à la vitesse spécifiée.
    @param vitesse la vitesse de déplacement (0-255)
    """
    set_pwm(IN1, vitesse)
    set_pwm(IN2, 0)
    set_pwm(IN3, vitesse)
    set_pwm(IN4, 0)


def recule(vitesse):
   """!
   Recule le robot à la vitesse spécifiée.
   @param vitesse la vitesse de recul (0-255)
   """
   set_pwm(IN1, 0)
   set_pwm(IN2, vitesse)
   set_pwm(IN3, 0)
   set_pwm(IN4, vitesse)

def droite(vitesse):
   """!
   Tourne le robot vers la droite à la vitesse spécifiée.
   @param vitesse la vitesse de rotation (0-255)
   """
   set_pwm(IN1, vitesse)
   set_pwm(IN2, 0)
   set_pwm(IN3, 0)
   set_pwm(IN4, vitesseRecul)

def gauche(vitesse):
    """!
    Tourne le robot vers la gauche à la vitesse spécifiée.
    @param vitesse la vitesse de rotation (0-255)
    """
    set_pwm(IN1, 0)
    set_pwm(IN2, vitesseRecul)
    set_pwm(IN3, vitesse)
    set_pwm(IN4, 0)

def droite90():
    """!
    Tourne le robot vers la droite 
    """
    print("droite90")
    set_pwm(IN1, 255)
    set_pwm(IN2, 0)
    set_pwm(IN3, 0)
    set_pwm(IN4, 255)
    time.sleep(0.35)

vitesseFindCube = 130
def droite10():
    """!
    Tourne le robot vers la droite
    """
    print("droite10")
    set_pwm(IN1, vitesseFindCube)
    set_pwm(IN2, 0)
    set_pwm(IN3, 0)
    set_pwm(IN4, vitesseFindCube)

    
def gauche90(): 
    """!
    Tourne le robot vers la gauche 
    """
    print("gauche90")
    set_pwm(IN1, 0)
    set_pwm(IN2, 170)
    set_pwm(IN3, 210)
    set_pwm(IN4, 0)
    time.sleep(0.35)
    stop()

def gauche10():
    """!
    Tourne le robot vers la gauche 
    """
    print("gauche10")
    set_pwm(IN1, 0)
    set_pwm(IN2, vitesseFindCube)
    set_pwm(IN3, vitesseFindCube)
    set_pwm(IN4, 0)
    
# Fonction pour récupérer la mission du robot
def getMission():
    """! Récupère la mission du robot depuis le serveur.
    @return None si la récupération échoue, sinon la liste des cubes à récupérer
    """
    try:
        reponse = urequests.get(f"http://{IpNous}/instructions?robot_id={UUID}")
        texte_json = reponse.text
        donnees = json.loads(texte_json)
        cubeARecup = donnees.get("rows", [])
        print("cube à récupérer" , cubeARecup)
    except Exception as e:
        print("Erreur de requête :", e)


def postTelemetry(vitesseRobot, dist, statusDeplacement, statusLigne, pinceValue, UUID):
    """! Envoie les données de télémétrie au serveur.
    @param vitesseRobot la vitesse actuelle du robot
    @param dist la distance mesurée par l'ultrason
    @param statusDeplacement le statut du déplacement (AVANCE, RECULE, etc.)
    @param statusLigne le statut de la ligne (1 pour suivi, 0 pour pas de suivi)
    @param pinceValue l'état de la pince (True pour ouverte, False pour fermée)
    @param UUID l'identifiant unique du robot
    """
    payload = {
        "vitesse": vitesseRobot,
        "distance_ultrasons": dist,
        "statut_deplacement": statusDeplacement,
        "ligne": statusLigne,
        "statut_pince": pinceValue,
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
         
          
# Fonction pour récupérer le cube
def getCubee() :
    """! Récupère le cube en avançant jusqu'à ce que la distance soit inférieure à 5 cm.
    Cette fonction arrête le robot, ferme la pince et attend 5 secondes avant de continuer.
    """
    global dist
    print("getCube")
    
    dist = mesure_distance()
    
    if dist < 0:
      dist = 40
      
    while dist > 5.0:
      avance(150)
      dist = mesure_distance()
      if dist < 0:
        dist = 40
      print("ditancee", dist)
    if 0 <= dist <= 5:
        stop()
        time.sleep(5)
        pinceValue = False
        pince(pinceValue)
        time.sleep(30)
     

# Fonction pour retourner sur la piste  
def returnPiste():
    """! Retourne sur la piste en reculant jusqu'à ce que les capteurs de ligne détectent à nouveau la piste.
    Cette fonction recule le robot jusqu'à ce que les capteurs de ligne détectent la piste, puis arrête le robot.
    """
    g, d = capteur_gauche.value(), capteur_droite.value()
    
    while g and d:
        print("recule")
        recule(120)
        
    
    
def getCube():
    """! Récupère le cube en avançant jusqu'à ce que la distance soit inférieure à 4 cm.
    Cette fonction arrête le robot, ferme la pince et attend 2 secondes avant de continuer.
    """
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
    
# Fonction pour trouver le cube
def findCube():
  """!
  Cherche le cube en tournant à droite jusqu'à ce que la distance soit inférieure à 30 cm.
  Si un cube est détecté à une distance inférieure ou égale à 25 cm, le robot s'arrête, tourne à droite trois fois, puis récupère le cube.
  """   
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
 
      
#  Suivi de ligne 
def suivre_ligne():
    """!
    Suivi de ligne en utilisant les capteurs gauche et droit.
    Cette fonction ajuste la direction du robot en fonction des valeurs des capteurs de ligne.
    Si les deux capteurs détectent la ligne, le robot s'arrête et cherche le cube.
    """
    global compteurLigne
    g, d = capteur_gauche.value(), capteur_droite.value()
  
    if g and d:      
        set_led_color(0, 255, 255,255)
        stop()
        time.sleep(0.5)
        findCube()
      
    elif d:
        stop()
        time.sleep(0)
        droite(vitesseLente)
        # print("Droite")
        set_led_color(2, 255, 128, 0)
    elif g:
        stop()
        time.sleep(0)
        gauche(vitesseLente)
        # print("Gauche")
        set_led_color(1, 255, 128, 0)
    else:
        avance(maxVitesse)
        # print("Avance")
        set_led_color(0, 0, 0, 0)


#  Fonction pour mesurer la distance avec l'ultrason
def mesure_distance():
    """! Mesure la distance à l'aide d'un capteur ultrason.
    @return la distance mesurée en centimètres, ou -1 en cas d'erreur
    """
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


#  Fonction de démarrage du robot
def start():
    """! Fonction de démarrage du robot.
    Cette fonction initialise le robot, connecte le Wi-Fi, configure la pince et les LEDs.
    """ 
    pince(False)
    time.sleep(0.5)
     
    clignoter_leds(255, 0, 0, 0.2)

start()
    
#  Boucle principale 
while True:
    #while True:   
    #dist = mesure_distance()
    #postTelemetry(vitesseRobot, dist, statusDeplacement, statusLigne, pinceValue, UUID)
    #time.sleep(1)
    suivre_ligne()

    time.sleep(0.05)  # plus réactif, sans surcharge