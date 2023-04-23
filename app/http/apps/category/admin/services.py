from app.vendors.dependencies import DB, Company
from sqlalchemy.orm.exc import NoResultFound
from fastapi import (
	HTTPException,
	status,
)
from enum import Enum
from sqlalchemy import desc
from app import models as mdl
from . import schemas as sch
from app.config import cfg



def get_categories(db: DB, company: Company, skip: int = 0, limit: int = cfg.items_in_list):
	select_categories = db.select(
			mdl.Category,
		).\
		filter_by(company_id=company.id).\
		offset(skip).limit(limit).\
		order_by(desc('created_at'))
	categories = db.session.execute(select_categories).scalars().all() 
	return categories


def get_category(db: DB, company: Company, category_id: int):
	category = mdl.Category.get_first_item_by_filter(db, id=category_id, company_id=company.id)
	if not category:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Category not found'
		)
	return category


def create_category(db: DB, company: Company, category_data: sch.CategoryInCreate):
	category = mdl.Category.get_first_item_by_filter(db, slug=category_data.slug, company_id=company.id)
	if category:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail='Category slug not unique',
		)
	new_category = mdl.Category(
		slug = category_data.slug,
		name = category_data.name,
		short_desc = category_data.short_desc,
		is_valid = category_data.is_valid,
		parent_id = category_data.parent_id,
		company_id = company.id,
	)
	db.session.add(new_category)
	db.session.commit()
	db.session.refresh(new_category)
	return new_category


def update_category(db: DB, company: Company, category_id: int, category_data: sch.CategoryInUpdate):
	category = mdl.Category.get_first_item_by_filter(db, id=category_id)
	if category is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail='Category not found',
		)
	select_not_unique_category = db.select(mdl.Category,).\
		filter(
			mdl.Category.company_id==company.id, 
			mdl.Category.slug==category_data.slug,
			mdl.Category.id!=category.id
		)
	cat_with_slug = db.session.execute(select_not_unique_category).scalar()
	if cat_with_slug:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail='Category slug not unique',
		)
	for field, value in category_data:
		setattr(category, field, value)
	db.session.add(category)
	db.session.commit()
	return category


def delete_category(db: DB, company: Company, category_id: int):
	category = mdl.Category.get_first_item_by_filter(db, id=category_id)
	if category is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Category not found'
		) from None
	db.session.delete(category)
	db.session.commit()


class FileWidth(int, Enum):
	thumbnail = cfg.image_width['THUMBNAIL']
	showcase  = cfg.image_width['SHOWCASE']
	slider    = cfg.image_width['SLIDER']
	logo      = cfg.image_width['LOGO']

async def async_upload_thumb(db: DB, company: Company, pk: int, file: None, width: int):
	category = mdl.Category.get_first_item_by_filter(db, id=pk, is_valid=True)
	if category is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Category not found'
		) from None
	try:
		ext_img_path = f'images/category/{pk}/thumb'
		img_path = category.save_and_resize_img(file, ext_img_path, width)
		file_path = None
		category.thumb = img_path
		db.session.add(category)
		db.session.commit()
		return {'success': f'File uploaded (Category:{pk})'}
	except:
		return {'error':'error'}