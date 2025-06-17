from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from controller import mainController
from controller.api import RobotController, InstructionsController, TelemetryController
from database import database

app = FastAPI()
app.include_router(RobotController.router)
app.include_router(InstructionsController.router)
app.include_router(TelemetryController.router)

app.include_router(mainController.router)
app.mount("/static", StaticFiles(directory="public"), name="static")

database.init_db()


# peut être séparer tout les fichiers et faire 

# un fichier robot repo qui fait que pour le robot 
# un fichier robot service qui fait que pour le robot
# un fichier robot controller qui fait que pour le robot

# un fichier commandes repo qui fait que pour les commandes
# un fichier commandes service qui fait que pour les commandes
# un fichier commandes controller qui fait que pour les commandes

# un fichier valeurs repo qui fait que pour les valeurs
# un fichier valeurs service qui fait que pour les valeurs
# un fichier valeurs controller qui fait que pour les valeurs

