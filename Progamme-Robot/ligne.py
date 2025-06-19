from machine import Pin
import time

capteur_gauche = Pin(26, Pin.IN)
capteur_droit = Pin(27, Pin.IN)

def lire_capteurs():
    etat_gauche = capteur_gauche.value()
    etat_droit = capteur_droit.value()
  
    print(f"droit {etat_droit}")
    print(f"gauche {etat_gauche}")
  
while True:
    lire_capteurs()
    time.sleep(0.2)
