from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from repository.RobotRepository import robotIdExists
from service.RobotService import fetchRobots, setRobotAndVerify

router = APIRouter()

# Route /robots pour récupérer tout les robots enregistrés
@router.get("/robots")
async def get_robots_endpoint():
    return {"rows": fetchRobots()}

# Rtoute /robotInitialize pour initialiser un robot
@router.post("/robotInitialize")
async def set_robots_endpoint(request: Request):
    try:
        body = await request.json()
        robotId = body.get("uuid")
        alias = body.get("alias")

        if not robotId:  # si robotId n'est pas envoyé
            return JSONResponse(status_code=400, content={"error": "robotId manquant"})

        if robotIdExists(robotId, alias): # Si le robot existe déjà 
            return JSONResponse(status_code=409, content={"error": "robot_id ou alias déjà utilisé"})

        setRobotAndVerify(robotId, alias)
        
        return JSONResponse(status_code=201, content={"status": "Robot ajouté avec succès"})

    except Exception as e:
        print(f"[ERREUR] {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

