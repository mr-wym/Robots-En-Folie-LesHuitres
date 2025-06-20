from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from service.TelemetryService import setTelemetryAndVerif, setSummaryAndVerif

router = APIRouter()

# Route /telemetry pour que le robot puisse envoyer ca telemetry toutes les seondes 
@router.post("/telemetry")
async def post_telemetry(request: Request):
    data = await request.json()
    vitesse = data.get("vitesse")
    dist = data.get("distance_ultrasons")
    statusDeplacement = data.get("statut_deplacement")
    statusLigne = data.get("ligne")
    pinceValue = data.get("statut_pince")
    uuidNous = data.get("robot_id")

    setTelemetryAndVerif(vitesse, dist, statusDeplacement, statusLigne, pinceValue, uuidNous)

    return {"message": "Telemetry ajouté"}

# Route /summary pour que le robot puisse envoyer son uuid pour renseigner que la mission est finie
@router.post("/summary")
async def post_summary(request: Request):
    data = await request.json()
    robot_id = data.get("robot_id")

    setSummaryAndVerif(robot_id)

    return {"message": "Summary ajouté"}




# @router.get("/gettelemetry")
# async def get_telemetry():
#     try:
#         rows = fetchTelemetry()
#         return JSONResponse(status_code=200, content={"rows": rows})
#     except Exception as e:
#         print(f"[ERREUR] {e}")
#         return JSONResponse(status_code=500, content={"error": str(e)})