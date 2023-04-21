from app.vendors.dependencies import DB, Company
from app.http.apps.auth import CurrentUser
from fastapi import (
    Depends, 
    APIRouter, 
    Response, 
    HTTPException,
    status, 
    Path,
)
from typing import Annotated
from . import policy as pls
from . import services as srv
from . import schemas as sch
from app.config import cfg


company = APIRouter(
    prefix = '/company',
    tags = ['company'], 
)


@company.get('/list/', 
    response_model=list[sch.CompanyIn], 
    status_code=status.HTTP_200_OK
)
async def read_companies(
    company: Company, db: DB, account: pls.CompanyShowList,
    skip: int = 0, limit: int = cfg.items_in_list,
):
    return srv.get_companies(db, skip=skip, limit=limit)


@company.get('/{pk}/show/', 
    response_model=sch.CompanyIn,
    status_code=status.HTTP_200_OK
)
async def read_company(
    company: Company, db: DB, account: pls.CompanyShowItem,
    pk: Annotated[int, Path(title="The ID company", gt=0)]
):
    return srv.get_company(db, company_id=pk)


@company.post('/create/', 
    response_model=sch.CompanyIn,
    status_code=status.HTTP_201_CREATED
)
async def create_company(
    company: Company, db: DB, account: pls.CompanyCreate,
    company_data: sch.CompanyInCreate
):
    return srv.create_company(db, company_data=company_data)


@company.put('/{pk}/update/', 
    response_model=sch.CompanyIn,
    status_code=status.HTTP_202_ACCEPTED
)
async def update_company(
    company: Company, db: DB, account: pls.CompanyUpdate,
    company_data: sch.CompanyInUpdate,
    pk: Annotated[int, Path(title="The ID company", gt=0)]
):
    return srv.update_company(db, company_id=pk, company_data=company_data)


@company.delete('/{pk}/delete/', 
    response_model=sch.CompanyIn,
)
async def delete_company(
    company: Company, db: DB, account: pls.CompanyDelete,
    pk: Annotated[int, Path(title="The ID company", gt=0)]
):
    srv.delete_company(db, company_id=pk)
    return Response(status_code=status.HTTP_204_NO_CONTENT)