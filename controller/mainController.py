from fastapi import APIRouter
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse, FileResponse

from repository.TelemetryRepository import getTelemetry, getTelemetryById
from repository.InstructionsRepository import getMissions, setMissions
from repository.RobotRepository import getRobotIdAlias, getRobots

router = APIRouter()


@router.get("/", response_class = HTMLResponse)
async def root(robot_selected: str = None):
    with open('templates/index.html', 'r', encoding='utf-8') as file:
        if robot_selected == None:
            robot_selected = "53d67923-704f-4b97-b6d4-64a0a04ca5de"

        html_content = file.read()
        aliases = getRobots()
        robot_id = robot_selected
        telemetry_aliases = getTelemetryById(robot_selected)
        # telemetry_aliases = getTelemetry()
        missions = getMissions(robot_selected)



        options_html = "".join([f'<option value="{alias[1]}" {"selected" if alias[1] == robot_id else ""}>{alias[2]}</option>' for alias in aliases])
        html_content = html_content.replace("<!--noms_robots-->", options_html)

        options_html = "".join([f'<p>{telemetry_aliases[0]}</p>' for alias in telemetry_aliases])
        html_content = html_content.replace("<!--noms_telemetrie-->", options_html)

        options_html = "".join([f'<p value="{str(alias)}">{alias}</p>' for alias in missions])
        html_content = html_content.replace("<!--all_missions-->", options_html)

        # options_html = "".join([f'<option value="{alias[1]}">{alias[2]}</option>' for alias in aliases])
        # html_content = html_content.replace("<!--OPTIONS_PLACEHOLDER-->", options_html)

    return HTMLResponse(content=html_content)
