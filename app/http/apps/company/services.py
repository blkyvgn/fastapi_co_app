from app.vendors.dependencies import DB, Company
from sqlalchemy.orm import exc
from sqlalchemy import func
from fastapi import (
	HTTPException,
	status,
)
from app import models as mdl
from . import schemas as sch
from app.config import cfg


async def get_company(db: DB, pk: int):
	select_company = db.select(
			mdl.Company.id, mdl.Company.alias, mdl.Company.name, mdl.Company.options,
			func.count(mdl.Article.id).label('articles_count'),
		).filter_by(id=pk).\
		outerjoin(mdl.Company.articles).\
		group_by(mdl.Company.id).\
		filter(mdl.Company.is_valid==True)
	try:
		company = db.session.execute(select_company).one()
	except exc.NoResultFound:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Company not found'
		)
	return company