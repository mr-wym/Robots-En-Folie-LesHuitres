from fastapi import APIRouter, Request
from flask import jsonify
from fastapi.responses import HTMLResponse
from service.RobotService import fetchValeurs, fetchCommandes, fetchRobots
from repository.RobotRepository import getValeurs

router = APIRouter()


@router.get("/api/valeurs")
async def get_valeurs_endpoint():
    return {"rows": fetchValeurs()}


@router.get("/api/commandes")
async def get_commandes_endpoint():
    return {"rows": fetchCommandes()}


@router.get("/api/robots")
async def get_robots_endpoint():
    return {"rows": fetchRobots()}
