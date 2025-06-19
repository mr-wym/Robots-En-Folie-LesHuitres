from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from service.InstructionsService import fetchMission, setMissionAndVerif
from repository.RobotRepository import getRobotIdAlias

router = APIRouter()

# Route /instrcutions qui renvoie la dernière mission en foncition de son robot_id
@router.get("/instructions")
async def get_commandes_endpoint(robot_id: str):
    blocks = fetchMission(robot_id)
    print("block", blocks)

    if blocks is None:
        return JSONResponse(content={"error": "Aucune mission trouvée pour ce robot."})

    return {"blocks": blocks}

# Route /setinstructions pour ajouter une mission pour un robot précis
@router.post("/setinstructions")
async def set_commandes_endpoint(request: Request):
    try:
        body = await request.json()
        datetime = body.get("datetime")
        mission = body.get("mission")
        uuid = body.get("uuid")
        alias = body.get("alias")

        if not uuid: # Si uuid n'est pas entré alors récupérer l'uuid du robot grace a son nom
            uuid = getRobotIdAlias(alias)

        if not datetime:
            datetime = datetime.now().isoformat()

        if not datetime or not mission or not uuid:
            return {"error": "datetime, mission et uuid sont requis"}, 400

        if not datetime or not mission or not uuid: # Si l'un des élements essentiel n'est pas renseigné retourner une erreur 
            print("datetime ou mission manquant")
            return JSONResponse(status_code=400, content={"error": "datatime ou mission ou uuid manquant"})
        
        setMissionAndVerif(datetime, mission, uuid)

        return JSONResponse(status_code=201, content={"status": "Mission ajoutée avec succès"})

    except Exception as e:
        print(f"[ERREUR] {e}")
        return {"error-InstructionsController": str(e)}, 500
