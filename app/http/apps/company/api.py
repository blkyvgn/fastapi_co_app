from app.vendors.base.router import AppRouter
from app.vendors.dependencies import DB, Company
from fastapi import (
    Depends, 
    APIRouter, 
    Response, 
    HTTPException,
    status, 
)
from . import services as srv
from . import schemas as sch
from app.config import cfg

company = APIRouter(
    route_class=AppRouter, 
    prefix = '/company',
    tags=['company']
)
from app import models as mdl
@company.get('/',
    response_model=sch.CompanyOutItem,
    status_code=status.HTTP_200_OK
)
async def read_item(company: Company, db: DB):
    company = await srv.get_company(db, pk=company.id)
    return company