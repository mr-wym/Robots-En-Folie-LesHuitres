from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class = HTMLResponse)
async def root():
    with open('templates/index.html', 'r') as file:
        return file.read()

    return {}  # Retour vide


@router.post("/robot/data")
async def receive_robot_data(request: Request):
    body = await request.json()

    # Extraction manuelle (sans modèle)
    speed = body.get("speed")
    distance = body.get("distance")
    orientation = body.get("orientation")
    gripper = body.get("gripper")
    timestamp = body.get("timestamp")


    return {}  # Retour vide
