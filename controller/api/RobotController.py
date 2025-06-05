from fastapi import APIRouter
from service.RobotService import fetchRobots

router = APIRouter()

@router.get("/api/robots")
async def get_robots_endpoint():
    return {"rows": fetchRobots()}
