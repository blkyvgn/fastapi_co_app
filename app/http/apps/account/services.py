from app.vendors.dependencies import DB, Company
from sqlalchemy.orm.exc import NoResultFound
from fastapi import (
	HTTPException,
	status,
)
from sqlalchemy import (
	func, 
	desc,
)
from app import models as mdl
from . import schemas as sch
from app.config import cfg


def get_accounts(db: DB, company: Company, skip: int = 0, limit: int = cfg.items_in_list):
	select_accounts = db.select(
			mdl.Account.id, mdl.Account.email, mdl.Account.username,
			mdl.Profile.first_name, mdl.Profile.last_name, 
			mdl.Profile.sex, mdl.Profile.photo,
			func.count(mdl.Article.id).label('articles_count')
		).\
		filter_by(is_valid=True, is_activated=True).\
		outerjoin(mdl.Account.articles).outerjoin(mdl.Account.profile).\
		group_by(mdl.Account.username).\
		offset(skip).limit(limit).\
		order_by(desc('created_at'))
	accounts = db.session.execute(select_accounts).all()
	return accounts


def get_account(db: DB, company: Company, account_id: int):
	select_account = db.select(
			mdl.Account.id, mdl.Account.email, mdl.Account.username,
			mdl.Profile.first_name, mdl.Profile.last_name, 
			mdl.Profile.sex, mdl.Profile.photo,
			func.count(mdl.Article.id).label('articles_count')
		).\
		filter_by(is_valid=True, is_activated=True).\
		filter_by(id=account_id).\
		outerjoin(mdl.Account.articles).outerjoin(mdl.Account.profile)
	try:
		account = db.session.execute(select_account).one()
	except NoResultFound:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Account not found'
		)
	return account