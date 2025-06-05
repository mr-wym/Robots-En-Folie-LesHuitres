from fastapi import APIRouter
from service.CommandeService import fetchCommandes

router = APIRouter()

@router.get("/api/commandes")
async def get_commandes_endpoint():
    return {"rows": fetchCommandes()}
