from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from repository.TelemetryRepository import getTelemetryById
from repository.InstructionsRepository import getAllMissions
from repository.RobotRepository import getRobots

router = APIRouter()

# Route / qui renvoie la page html de l'IHM qui affiche les inforation de le telemetry d'un robot et ses missions
@router.get("/", response_class = HTMLResponse)
async def root(robot_selected: str = None):
    with open('templates/index.html', 'r', encoding='utf-8') as file:

        if robot_selected == None: # Si pas définie alors par défault prendre l'uuid de notre robot 
            robot_selected = "53d67923-704f-4b97-b6d4-64a0a04ca5de"

        html_content = file.read()
        aliases = getRobots()
        robot_id = robot_selected
        telemetry_aliases = getTelemetryById(robot_selected)
        missions = getAllMissions(robot_selected)

        options_html = "".join([f'<option value="{alias[1]}" {"selected" if alias[1] == robot_id else ""}>{alias[2]}</option>' for alias in aliases])
        html_content = html_content.replace("<!--noms_robots-->", options_html)

        options_html = "".join([f'<option value="{telemetry[0]}">{telemetry[1]}</option>' for telemetry in telemetry_aliases])
        html_content = html_content.replace("<!--telemetry-->", options_html)

        if missions is not None:
            html_content = html_content.replace("<!--all_missions-->", f"<p>Mission courante : {missions}</p>")
        else:
            html_content = html_content.replace("<!--all_missions-->", "<p>Aucune mission trouvée</p>")

    return HTMLResponse(content=html_content)
