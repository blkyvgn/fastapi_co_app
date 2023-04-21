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

category = APIRouter(
    route_class=AppRouter, 
    prefix = '/category',
    tags = ['category'], 
)


@category.get('/list/', 
    response_model=list[sch.CategoryOut],
    status_code=status.HTTP_200_OK
)
async def read_categories(
    company: Company, db: DB,
    skip: int = 0, limit: int = cfg.items_in_list
):
    return srv.get_categories(db, company, skip=skip, limit=limit)


@category.get('/{pk}/show/', 
    response_model=sch.CategoryOut,
    status_code=status.HTTP_200_OK
)
async def read_category(
    company: Company, db: DB,
    pk: Annotated[int, Path(title="The ID category", gt=0)]
):
    return srv.get_category(db, company, category_id=pk)