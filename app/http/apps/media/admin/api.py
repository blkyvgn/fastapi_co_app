from app.vendors.dependencies import DB, Company
from app.vendors.base.router import AppRouter
from fastapi import (
	Depends, 
	APIRouter, 
	Response, 
	HTTPException,
	status, 
	Path,
	File, 
	UploadFile,
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


@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
	return {"filenames": [file.filename for file in files]}