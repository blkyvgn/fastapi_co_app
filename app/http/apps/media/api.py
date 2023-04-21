from app.vendors.dependencies import DB, Company
from app.vendors.base.router import AppRouter
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