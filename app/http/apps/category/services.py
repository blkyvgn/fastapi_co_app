from app.vendors.dependencies import DB, Company
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import exc
from sqlalchemy import func
from fastapi import (
	HTTPException,
	status,
)
from sqlalchemy import (
	func, 
	desc,
	and_,
)
from sqlalchemy.orm import aliased
from sqlalchemy.orm import joinedload
from app import models as mdl
from . import schemas as sch
from app.config import cfg


def get_categories(db: DB, company: Company, skip: int = 0, limit: int = cfg.items_in_list):
	select_categories = db.select(
			mdl.Category,
		).\
		filter_by(is_valid=True, company_id=company.id).\
		offset(skip).limit(limit).\
		order_by(desc('created_at'))
	categories = db.session.execute(select_categories).scalars().all() 
	return categories

def get_category(db: DB, company: Company, category_id: int):
	category = mdl.Category.get_first_item_by_filter(db, 
		is_valid=True, id=category_id, company_id=company.id
	)
	if not category:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Category not found'
		)
	return category