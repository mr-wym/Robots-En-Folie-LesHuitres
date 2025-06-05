from fastapi import APIRouter, Request
from service.CommandeService import fetchCommandes

router = APIRouter()

@router.get("/api/commandes")
async def get_commandes_endpoint():
    return {"rows": fetchCommandes()}

@router.post("/api/commandeInitialize")
async def set_commandes_endpoint(request: Request):
    try:
        body = await request.json()
        datetime = body.get("datetime")
        commande = body.get("commande")

        if not datetime or not commande:
            return {"error": "datetime and commande are required"}, 400

        from repository.CommandeRepository import setCommandes
        setCommandes(datetime, commande)

        print("Commande enregistrée avec succès")
        
        return {"status": "success"}

    except Exception as e:
        print(f"[ERREUR] {e}")
        return {"error": str(e)}, 500
