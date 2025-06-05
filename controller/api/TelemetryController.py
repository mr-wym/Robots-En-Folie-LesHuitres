from fastapi import APIRouter
from service.TelemetryService import fetchValeurs

router = APIRouter()

@router.get("/api/valeurs")
async def get_valeurs_endpoint():
    return {"rows": fetchValeurs()}
