from app.vendors.dependencies import DB, Company
from starlette.responses import StreamingResponse
from app.vendors.base.router import AppRouter
from starlette.requests import Request
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


@media.get('/video/{pk}/stream/')
async def get_streaming_video(
	company: Company, db: DB, request: Request, 
	pk: Annotated[int, Path(title="The ID media", gt=0)]
) -> StreamingResponse:
	file, status_code, content_length, headers = await srv.open_file(request, db, video_id)
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