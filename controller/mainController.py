from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class = HTMLResponse)
async def root():
    with open('templates/index.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    return HTMLResponse(content=html_content)
