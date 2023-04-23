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


article = APIRouter(
    prefix = '/article',
    tags = ['article'], 
)


# @category.get('/list/', 
#     response_model=list[sch.CategoryIn], 
#     status_code=status.HTTP_200_OK
# )
# async def read_companies(
#     company: Company, db: DB, account: pls.CategoryShowList,
#     skip: int = 0, limit: int = cfg.items_in_list,
# ):
#     return srv.get_categories(db, company, skip=skip, limit=limit)


# @category.get('/{pk}/show/', 
#     response_model=sch.CategoryIn,
#     status_code=status.HTTP_200_OK
# )
# async def read_category(
#     company: Company, db: DB, account: pls.CategoryShowItem,
#     pk: Annotated[int, Path(title="The ID category", gt=0)]
# ):
#     return srv.get_category(db, company,  category_id=pk)


# @category.post('/create/', 
#     response_model=sch.CategoryIn,
#     status_code=status.HTTP_201_CREATED
# )
# async def create_category(
#     company: Company, db: DB, account: pls.CategoryCreate,
#     category_data: sch.CategoryInCreate
# ):
#     return srv.create_category(db, company, category_data=category_data)


# @category.put('/{pk}/update/', 
#     response_model=sch.CategoryIn,
#     status_code=status.HTTP_202_ACCEPTED
# )
# async def update_category(
#     company: Company, db: DB, account: pls.CategoryUpdate,
#     category_data: sch.CategoryInUpdate,
#     pk: Annotated[int, Path(title="The ID category", gt=0)]
# ):
#     return srv.update_category(db, company, category_id=pk, category_data=category_data)


# @category.delete('/{pk}/delete/', 
#     response_model=sch.CategoryIn,
# )
# async def delete_category(
#     company: Company, db: DB, account: pls.CategoryDelete,
#     pk: Annotated[int, Path(title="The ID company", gt=0)]
# ):
#     srv.delete_category(db, company, category_id=pk)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


@article.post('/{pk}/upload-thumb/',
    status_code=status.HTTP_200_OK
)
async def upload_thumb(
    company: Company, db: DB,
    pk: Annotated[int, Path(title="The ID company", gt=0)], 
    file: UploadFile, 
    width: int
):
    return await srv.async_upload_thumb(db, company, pk, file, width)