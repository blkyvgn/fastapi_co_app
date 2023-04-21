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

account = APIRouter(
    route_class=AppRouter, 
    prefix = '/account',
    tags = ['account'], 
)


@account.get('/list/', 
    response_model=list[sch.AccountOut],
    status_code=status.HTTP_200_OK
)
async def read_accounts(
    company: Company, db: DB,
    skip: int = 0, limit: int = cfg.items_in_list
):
    return srv.get_accounts(db, company, skip=skip, limit=limit)


@account.get('/{pk}/show/', 
    response_model=sch.AccountOut,
    status_code=status.HTTP_200_OK
)
async def read_account(
    company: Company, db: DB,
    pk: Annotated[int, Path(title="The ID account", gt=0)]
):
    return srv.get_account(db, company, account_id=pk)