from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from repository.CommandeRepository import commandeExists
from service.CommandeService import fetchCommandes
from repository.RobotRepository import getMacAddressAlias

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
        macAddress = body.get("macAddress")
        alias = body.get("alias")

        print(f"macaddress before = {macAddress}")
        print(f"macAddress = {macAddress} (type: {type(macAddress)})")

        if not macAddress:
            macAddress = getMacAddressAlias(alias)

        print(f"macaddress after = {macAddress}")
        print(f"macAddress = {macAddress} (type: {type(macAddress)})")



        if not datetime or not commande or not macAddress:
            return {"error": "datetime, commande et macAddress sont requis"}, 400

        from repository.CommandeRepository import setCommandes

        if not datetime or not commande or not macAddress:
            print("datetime ou commande manquant")
            return JSONResponse(status_code=400, content={"error": "datatime ou commande ou macAddress manquant"})
        
        print(f"datetime = {datetime}")
        print(f"commande = {commande}")
        print(f"alias = {alias}")
        print(f"macaddress = {macAddress}")



        # if commandeExists(datetime, commande, macAddress):
        if commandeExists(datetime, commande, macAddress):
            return JSONResponse(status_code=409, content={"error": "Commande déjà enregistrée pour ce robot."})

        setCommandes(datetime, commande, macAddress)

        print("Commande enregistrée avec succès")
        
        return JSONResponse(status_code=201, content={"status": "Commande ajoutée avec succès"})
    

    except Exception as e:
        print(f"[ERREUR] {e}")
        return {"error": str(e)}, 500
