from app.vendors.dependencies import DB, Company
from starlette.responses import StreamingResponse
from app.vendors.base.router import AppRouter
from starlette.requests import Request
from fastapi.responses import HTMLResponse
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
from . import services as srv
from . import schemas as sch
from .utils import open_file
from app.config import cfg

media = APIRouter(
	route_class=AppRouter, 
	prefix = '/media',
	tags = ['media'], 
)


@media.get('/list/', 
	response_model=list[sch.MediaOut],
	status_code=status.HTTP_200_OK
)
async def read_medias(
	company: Company, db: DB,
	skip: int = 0, limit: int = cfg.items_in_list
):
	return srv.get_medias(db, company, skip=skip, limit=limit)


@media.get('/{pk}/show/', 
	response_model=sch.MediaOut,
	status_code=status.HTTP_200_OK
)
async def read_media(
	company: Company, db: DB,
	pk: Annotated[int, Path(title="The ID media", gt=0)]
):
	return srv.get_media(db, company, media_id=pk)



templates = Jinja2Templates(directory='app/resources/test')

@media.get("/test/video/{id}", response_class=HTMLResponse)
async def test_video(request: Request, id: str):
	return templates.TemplateResponse('test_video.html', {'request': request, 'id': id})


@media.get('/video/{pk}/stream/')
async def get_streaming_video(
	company: Company, db: DB, request: Request, 
	pk: Annotated[int, Path(title="The ID media", gt=0)]
) -> StreamingResponse:
	file, status_code, content_length, headers = await open_file(request, db, pk)
	response = StreamingResponse(
		file,
		media_type='video/mp4',
		status_code=status_code,
	)

	response.headers.update({
		'Accept-Ranges': 'bytes',
		'Content-Length': str(content_length),
		**headers,
	})
	return response