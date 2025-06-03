from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from controller import RobotController
from database import database

app = FastAPI()
app.include_router(RobotController.router)
app.mount("/static", StaticFiles(directory="public"), name="static")

database.init_db()