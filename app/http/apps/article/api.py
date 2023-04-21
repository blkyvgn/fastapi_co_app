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

article = APIRouter(
    route_class=AppRouter, 
    prefix = '/article',
    tags = ['article'], 
)


@article.get('/list/', 
    response_model=list[sch.ArticleOut],
    status_code=status.HTTP_200_OK
)
async def read_articles(
    company: Company, db: DB,
    skip: int = 0, limit: int = cfg.items_in_list
):
    return srv.get_articles(db, company, skip=skip, limit=limit)


@article.get('/{pk}/show/', 
    response_model=sch.ArticleOut,
    status_code=status.HTTP_200_OK
)
async def read_article(
    company: Company, db: DB,
    pk: Annotated[int, Path(title="The ID article", gt=0)]
):
    return srv.get_article(db, company, article_id=pk)