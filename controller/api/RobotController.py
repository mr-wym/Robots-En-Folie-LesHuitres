from urllib import request
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from repository.RobotRepository import robotIdExists, setRobots
from service.RobotService import fetchRobots

router = APIRouter()

@router.get("/robots")
async def get_robots_endpoint():
    return {"rows": fetchRobots()}

@router.post("/robotInitialize")
async def set_robots_endpoint(request: Request):
    try:
        body = await request.json()
        robotId = body.get("macAddress")
        alias = body.get("alias")
        print(f"Id robot reçue : {robotId}")
        print(f"Alias reçu : {alias}")

        if not robotId:
            print("MAC manquante")
            return JSONResponse(status_code=400, content={"error": "robotId manquant"})

        if robotIdExists(robotId, alias):
            return JSONResponse(status_code=409, content={"error": "Adresse MAC ou Alias déjà utilisé."})

        setRobots(robotId, alias)
        
        return JSONResponse(status_code=201, content={"status": "Robot ajouté avec succès"})


    except Exception as e:
        print(f"[ERREUR] {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

