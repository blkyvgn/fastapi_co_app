from app.vendors.dependencies import DB, Company
from app.http.apps.auth.utils.jwt import create_token
from app.services.celery.tasks import send_email
from app.vendors.helpers import mail as m
from app.tasks.logger import write_to_log
from fastapi import (
	Request,
	HTTPException,
	BackgroundTasks,
	status,
)
import base64
from sqlalchemy import or_
from app import models as mdl
from . import schemas as sch
from app.config import cfg



def logger(background_tasks, username, message):
	background_tasks.add_task(write_to_log, username, message)
	

def register_new_user(request: Request, db: DB, account_data: sch.AccountCreate) -> sch.Token:
	account = mdl.Account.get_first_item_by_filter(
		db, _or=True, email=account_data.email, username=account_data.username
	)
	if account is not None:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail='Username or email not unique',
			headers={'WWW-Authenticate': 'Bearer'},
		)

	account = mdl.Account(
		email=account_data.email,
		username=account_data.username,
		is_valid=account_data.is_valid,
		password=mdl.Account.get_hashed_password(account_data.password),
	)
	db.session.add(account)
	db.session.commit()
	db.session.refresh(account)

	profile = mdl.Profile(
		first_name=account_data.profile.first_name,
		last_name=account_data.profile.first_name,
		female=account_data.profile.female,
		account_id=account.id,
	)
	db.session.add(profile)
	db.session.commit()

	if cfg.activated_account_by_email:
		account.send_activation_mail(request)

	return create_token(account)


def authenticate_user(db: DB, username: str, password: str) -> sch.Token:
	account = mdl.Account.get_first_item_by_filter(db, username=username)
	if not account or not account.verify_password(password):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail='Incorrect username or password',
			headers={'WWW-Authenticate': 'Bearer'},
		)
	if not account.is_activated:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, 
			detail='Not activated user',
			headers={'WWW-Authenticate': 'Bearer'},
		)
	if account.is_valid:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, 
			detail='Blocked user',
			headers={'WWW-Authenticate': 'Bearer'},
		)
	return create_token(account)


def activate_account(db: DB, uid: str, token: str) -> None:
	raw_uid = eval(base64.b64decode(uid))['uid']
	account_id = int(raw_uid.split(':')[0])
	account = mdl.Account.get_first_item_by_filter(db, id=account_id)
	account.is_activated = True
	db.session.add(account)
	db.session.commit()

# def write_notification(acc, req):
# 	acc.send_reset_passwd_mail(req)

# def account_email_check(request: Request, db: DB, bg_tasks: BackgroundTasks, account_email: sch.AccountEmail) -> sch.AccountEmail:
# 	account = mdl.Account.get_first_item_by_filter(
# 		db, email=account_email.email, is_activated=True, is_valid=True
# 	)
# 	if account is None:
# 		raise HTTPException(
# 			status_code=status.HTTP_404_NOT_FOUND, 
# 			detail='Account not found (or not valid or not activated)'
# 		)
# 	if not account.is_activated or not account.is_valid:
# 		raise HTTPException(
# 			status_code=status.HTTP_400_BAD_REQUEST, 
# 			detail='Not activated or not valid account',
# 			headers={'WWW-Authenticate': 'Bearer'},
# 		)
# 	bg_tasks.add_task(write_notification, account, request)
# 	# account.send_reset_passwd_mail(request)
# 	return account_email


# def confirm_reset_password(db: DB, uid: str, token: str):
# 	pass


# def change_password(db: DB, reset_passwd: sch.ResetPassword) -> bool:
# 	raw_uid = eval(base64.b64decode(uid))['uid']
# 	account_id = int(raw_uid.split(':')[0])
# 	account = mdl.Account.get_first_item_by_filter(db, id=account_id)
# 	account.password=mdl.Account.get_hashed_password(reset_passwd.password)
# 	db.session.add(account)
# 	db.session.commit()
# 	db.session.refresh(account)



