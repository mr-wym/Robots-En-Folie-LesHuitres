from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
# from service.TelemetryService import fetchTelemetry
from service.TelemetryService import fetchTelemetry, setTelemetryAndVerif, setSummaryAndVerif, setSummaryFinishAndVerif

router = APIRouter()
@router.post("/telemetry")
async def post_telemetry(request: Request):
    data = await request.json()
    vitesse = data.get("vitesse")
    distance_ultrason = data.get("distance_ultrason")
    status_deplacement = data.get("status_deplacement")
    ligne = data.get("ligne")
    pince_active = data.get("pince_active")
    robot_id = data.get("robot_id")

    setTelemetryAndVerif(vitesse, distance_ultrason, status_deplacement, ligne, pince_active, robot_id)

    return {"message": "Telemetry set successfully"}


router = APIRouter()
@router.post("/summary")
async def post_summary(request: Request):
    data = await request.json()
    robot_id = data.get("robot_id")

    setSummaryFinishAndVerif(robot_id)

    return {"message": "Summary set successfully"}


# @router.get("/gettelemetry")
# async def get_telemetry():
#     try:
#         rows = fetchTelemetry()
#         return JSONResponse(status_code=200, content={"rows": rows})
#     except Exception as e:
#         print(f"[ERREUR] {e}")
#         return JSONResponse(status_code=500, content={"error": str(e)})