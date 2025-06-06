from fastapi import APIRouter
from service.TelemetryService import fetchTelemetry

router = APIRouter()

@router.get("/api/telemetry")
async def get_valeurs_endpoint():
    return {"rows": fetchTelemetry()}
