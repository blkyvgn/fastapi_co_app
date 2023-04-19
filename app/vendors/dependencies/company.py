from fastapi import Depends, HTTPException
from sqlalchemy.orm.exc import NoResultFound
from fastapi_cache.decorator import cache
from collections import namedtuple
from .database import DB
from typing import Annotated
from app import models as mdl
from app.config import cfg

CompanyTuple = namedtuple('CompanyTuple', ['id', 'alias'])

# @cache(expire=cfg.cache_timeout['year'])
async def get_company(db: DB): # alias: str = cfg.company_alias
	try:
		alias = cfg.company_alias
		company = db.session.execute(
			db.select(mdl.Company.id, mdl.Company.alias).filter_by(alias='grkr', is_valid=True)
		).one()
	except NoResultFound:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Company not found'
		)
	company = CompanyTuple(company.id, company.alias)
	return company

Company = Annotated[CompanyTuple, Depends(get_company)]

