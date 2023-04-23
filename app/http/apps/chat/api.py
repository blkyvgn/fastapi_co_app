from app.vendors.dependencies import DB, Company
from starlette.responses import StreamingResponse
from app.vendors.base.router import AppRouter
from starlette.requests import Request
from fastapi.responses import HTMLResponse
from fastapi import WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import (
	Depends, 
	APIRouter, 
	Response, 
	HTTPException,
	status, 
	Path,
)
from typing import Annotated
# from . import services as srv
# from . import schemas as sch
from app.config import cfg

chat = APIRouter(
	route_class=AppRouter, 
	prefix = '/chat',
	tags = ['chat'], 
)


templates = Jinja2Templates(directory='app/resources/test')

@chat.get('/test/chat/{id}/', response_class=HTMLResponse)
async def test_video(request: Request, id: str):
	return templates.TemplateResponse('test_chat.html', {'request': request, 'id': id})


@chat.websocket('/ws/{room}/')
async def websocket_endpoint(websocket: WebSocket):
	await websocket.accept()
	while True:
		data = await websocket.receive_text()
		await websocket.send_text(f"Message text was: {data}")
