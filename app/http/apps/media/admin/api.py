from app.vendors.dependencies import DB, Company
from app.http.apps.auth import CurrentUser
from fastapi import (
	Depends, 
	APIRouter, 
	Response, 
	HTTPException,
	status, 
	Path,
	File, 
	UploadFile,
	BackgroundTasks,
	Form,
)
from typing import Annotated
from . import policy as pls
from . import services as srv
from . import schemas as sch
from app.config import cfg


media = APIRouter(
	prefix = '/media',
	tags = ['media'], 
)


@media.post('/{pk}/upload-video/',
	status_code=status.HTTP_200_OK
)
async def upload_video(
	company: Company, db: DB,
	pk: Annotated[int, Path(title="The ID media", gt=0)], 
	file: UploadFile
):
	return await srv.async_upload_video(db, company, pk, file)