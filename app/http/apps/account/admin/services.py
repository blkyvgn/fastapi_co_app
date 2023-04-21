from app.vendors.dependencies import DB, Company
from sqlalchemy.orm.exc import NoResultFound
from fastapi import (
	HTTPException,
	status,
)
from sqlalchemy import (
	func, 
	desc,
	and_,
	or_,
)
from app import models as mdl
from . import schemas as sch
from app.config import cfg


def get_accounts(db: DB, company: Company, skip: int = 0, limit: int = cfg.items_in_list):
	select_accounts = db.select(mdl.Account).\
		offset(skip).limit(limit).\
		order_by(desc('created_at'))
	accounts = db.session.execute(select_accounts).scalars().all() 
	return accounts


def get_account(db: DB, company: Company, account_id: int):
	account = mdl.Account.get_first_item_by_filter(db, id=account_id)
	if account is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Account not found'
		)
	return account


def create_account(db: DB, company: Company, account_data: sch.AccountInCreateUpdate):
	account = mdl.Account.get_first_item_by_filter(
		db, _or=True, email=account_data.email, username=account_data.username
	)
	if account is not None:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail='Username or email not unique',
		) from None

	new_account = mdl.Account(
		email=account_data.email,
		username=account_data.username,
		is_valid=account_data.is_valid,
		password=mdl.Account.get_hashed_password(account_data.password),
	)
	db.session.add(new_account)
	db.session.commit()
	db.session.refresh(new_account)

	new_profile = mdl.Profile(
		first_name=account_data.profile.first_name,
		last_name=account_data.profile.first_name,
		sex=account_data.profile.sex,
		account_id=new_account.id,
	)
	db.session.add(new_profile)
	db.session.commit()
	return new_account


def create_account_form(db: DB, company: Company, bg_task, account_data: sch.AccountInCreateUpdate, photo):
	account = mdl.Account.get_first_item_by_filter(
		db, _or=True, email=account_data.email, username=account_data.username
	)
	if account is not None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail='Username or email not unique',
		) from None

	new_account = mdl.Account(
		email=account_data.email,
		username=account_data.username,
		is_valid=account_data.is_valid,
		password=mdl.Account.get_hashed_password(account_data.password),
	)
	db.session.add(new_account)
	db.session.commit()
	db.session.refresh(new_account)

	profile_data = account_data.profile
	if profile_data:
		new_profile = mdl.Profile(
			first_name=profile_data.first_name,
			last_name=profile_data.first_name,
			sex=profile_data.sex,
			account_id=new_account.id,
		)
		if photo:
			ext_photo_path = f'images/account/{account_data.username}/profile'
			bg_task.add_task(mdl.Profile.save_and_resize_photo, photo, ext_photo_path, cfg.photo_width)
			# photo_file_subpath = mdl.Profile.save_and_resize_photo(photo, ext_photo_path, cfg.photo_width)
			# new_profile.photo=photo_file_subpath
			new_profile.photo=f'{ext_photo_path}/{photo.filename}'
		db.session.add(new_profile)
		db.session.commit()

		return new_account


def update_account(db: DB, company: Company, account_id: int, account_data: sch.AccountInCreateUpdate):
	account = mdl.Account.get_first_item_by_filter(db, id=account_id)
	if account is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Account not found'
		) from None

	select_not_unique_account = db.select(mdl.Account,).\
		filter(
			or_(
				mdl.Account.email==account_data.slug,
				mdl.Account.username==account_data.slug
			),
			mdl.Account.id!=account.id
		)
	account_with_email_username = db.session.execute(select_not_unique_account).scalar()
	if account_with_email_username:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail='Account email or username not unique',
		)
	
	account.email=account_data.email
	account.username=account_data.username
	account.is_valid=account_data.is_valid
	account.password=mdl.Account.get_hashed_password(account_data.password)
	db.session.add(account)
	db.session.commit()
	db.session.refresh(account)

	profile = mdl.Profile.get_first_item_by_filter(db, account_id=account.id)
	if profile is not None:
		profile_data = account_data.profile
		if profile_data:
			profile.first_name=profile_data.first_name
			profile.last_name=profile_data.first_name
			profile.sex=profile_data.sex
			db.session.add(profile)
			db.session.commit()
	return account


def delete_account(db: DB, company: Company, account_id: int):
	account = mdl.Account.get_first_item_by_filter(db, id=account_id)
	if not account:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Account not found'
		) from None
	profile = mdl.Profile.get_first_item_by_filter(db, account_id=account.id)
	if profile is not None:
		db.session.delete(profile)
	# account.delete(synchronize_session=False)
	db.session.delete(account)
	db.session.commit()