from app.vendors.dependencies import DB, Company
from sqlalchemy.orm import exc
from sqlalchemy import func
from fastapi import (
	HTTPException,
	status,
)
import inspect
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


def upload_file(db: DB, company: Company, item_key: str, item_pk: int, img_name: str, file, bg_task, width):
	item_key = item_key.capitalize()
	if model_cls := mdl.__dict__.get(item_key, None):
		if inspect.isclass(model_cls):
			item_obj = model_cls.get_first_item_by_filter(db, id=item_pk, is_valid=True)
			if item_obj is None:
				raise HTTPException(
					status_code=status.HTTP_404_NOT_FOUND, 
					detail=f'{item_key} not found'
				) from None
			bg_task.add_task(item_obj.upload_file, 'thumb', file, width)
			db.session.add(item_obj)
			db.session.commit()
			return {'success': f'File uploaded ({item_key}:{item_pk})'}
	return {'error':'error'}


async def async_upload_file(db: DB, company: Company, item_key: str, item_pk: int, img_name: str, file, bg_task, width):
	item_key = item_key.capitalize()
	if model_cls := mdl.__dict__.get(item_key, None):
		if inspect.isclass(model_cls):
			item_obj = model_cls.get_first_item_by_filter(db, id=item_pk, is_valid=True)
			if item_obj is None:
				raise HTTPException(
					status_code=status.HTTP_404_NOT_FOUND, 
					detail=f'{item_key} not found'
				) from None
			if hasattr(item_obj, img_name):
				try:
					file_path = await item_obj.async_upload_file(img_name, file, width)
					print(file_path)
				except:
					file_path = None
				setattr(item_obj, img_name, file_path)
				db.session.add(item_obj)
				db.session.commit()
				return {'success': f'File uploaded ({item_key}:{item_pk})'}
	return {'error':'error'}