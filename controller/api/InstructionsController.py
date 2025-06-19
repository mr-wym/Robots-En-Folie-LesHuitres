from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from repository.InstructionsRepository import missionExists, setMissions
from service.InstructionsService import fetchMission
from repository.RobotRepository import getRobotIdAlias
from datetime import datetime

router = APIRouter()

@router.get("/instructions")
async def get_commandes_endpoint(robot_id: str):
    print(f"robot_id = {robot_id}")
    blocks = fetchMission(robot_id)
    print("blok", blocks)

    if blocks is None:
        return JSONResponse(content={"error": "Aucune mission trouvée pour ce robot."})

    return {"blocks": blocks}

@router.post("/setinstructions")
async def set_commandes_endpoint(request: Request):
    try:
        body = await request.json()
        datetime = body.get("datetime")
        mission = body.get("mission")
        macAddress = body.get("macAddress")
        alias = body.get("alias")

        print(f"macaddress before = {macAddress}")

        if not macAddress:
            macAddress = getRobotIdAlias(alias)

        print(f"macaddress after = {macAddress}")

        if not datetime:
            datetime = datetime.now().isoformat()

        if not datetime or not mission or not macAddress:
            return {"error": "datetime, mission et macAddress sont requis"}, 400


        if not datetime or not mission or not macAddress:
            print("datetime ou mission manquant")
            return JSONResponse(status_code=400, content={"error": "datatime ou mission ou macAddress manquant"})
        
        print(f"datetime = {datetime}")
        print(f"mission = {mission}")
        print(f"alias = {alias}")

        # if missionExists(datetime, commande, macAddress):
        # if missionExists(datetime, mission, macAddress):
        #     return JSONResponse(status_code=409, content={"error": "Mission déjà enregistrée pour ce robot."})

        setMissions(datetime, mission, macAddress)

        print("Mission enregistrée avec succès")
        
        return JSONResponse(status_code=201, content={"status": "Mission ajoutée avec succès"})
    

    except Exception as e:
        print(f"[ERREUR] {e}")
        return {"error-InstructionsController": str(e)}, 500
