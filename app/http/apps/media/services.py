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


def get_medias(db: DB, company: Company, skip: int = 0, limit: int = cfg.items_in_list):
	select_medias = db.select(
			mdl.Media,
		).\
		filter_by(is_valid=True, company_id=company.id).\
		offset(skip).limit(limit).\
		order_by(desc('created_at'))
	medias = db.session.execute(select_medias).scalars().all() 
	return medias

def get_media(db: DB, company: Company, media_id: int):
	media = mdl.Media.get_first_item_by_filter(db, 
		is_valid=True, id=media_id, company_id=company.id
	)
	if not media:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Media not found'
		)
	return media