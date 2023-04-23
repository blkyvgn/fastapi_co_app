from app.vendors.base.router import AppRouter
from app.vendors.dependencies import DB, Company
from fastapi.responses import HTMLResponse
from fastapi import (
    Depends, 
    APIRouter, 
    Response, 
    HTTPException,
    status, 
    File, 
    UploadFile,
    BackgroundTasks,
    Form,
)
from enum import Enum
from typing import Annotated
from . import services as srv
from . import schemas as sch
from app import models as mdl
from app.config import cfg

company = APIRouter(
    route_class=AppRouter, 
    prefix = '/company',
    tags=['company']
)


@company.get('/',
    response_model=sch.CompanyOutItem,
    status_code=status.HTTP_200_OK
)
async def read_item(company: Company, db: DB):
    company = await srv.get_company(db, pk=company.id)
    return company

class FileWidth(int, Enum):
    thumbnail = cfg.image_width['THUMBNAIL']
    showcase  = cfg.image_width['SHOWCASE']
    slider    = cfg.image_width['SLIDER']
    logo      = cfg.image_width['LOGO']

@company.post('/uploadfile/',
    status_code=status.HTTP_200_OK
)
async def create_upload_file(
    company: Company, db: DB, bg_tasks: BackgroundTasks,
    item_key: str, item_pk: int, img_name: str, file: UploadFile, 
    width: FileWidth
):
    # return srv.upload_file(db, company, item_key, item_pk, file, bg_tasks, width)
    return await srv.async_upload_file(db, company, item_key, item_pk, img_name, file, bg_tasks, width)


@company.get("/test/")
async def main():
    content = """
<h1>Hello html str</h1>
    """
    return HTMLResponse(content=content)

