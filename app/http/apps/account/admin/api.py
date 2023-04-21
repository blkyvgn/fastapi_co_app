from app.vendors.dependencies import DB, Company
from app.http.apps.auth import CurrentUser
from fastapi import (
	Depends, 
	APIRouter, 
	Response, 
	HTTPException,
	status, 
	File, 
	Path,
	UploadFile,
	Form,
	BackgroundTasks,
)
from typing import Annotated
from . import policy as pls
from . import services as srv
from . import schemas as sch
from . import forms as frm
from app.config import cfg


account = APIRouter(
	prefix = '/account',
	tags = ['account'], 
)


@account.get('/list/', 
	response_model=list[sch.AccountIn], 
	status_code=status.HTTP_200_OK
)
async def read_companies(
	company: Company, db: DB, account: pls.AccountShowList,
	skip: int = 0, limit: int = cfg.items_in_list,
):
	return srv.get_accounts(db, company, skip=skip, limit=limit)


@account.get('/{pk}/show/', 
	response_model=sch.AccountIn,
	status_code=status.HTTP_200_OK
)
async def read_account(
	company: Company, db: DB, account: pls.AccountShowItem,
	pk: Annotated[int, Path(title="The ID account", gt=0)]
):
	return srv.get_account(db, company,  account_id=pk)


@account.post('/create/', 
	response_model=sch.AccountIn,
	status_code=status.HTTP_201_CREATED
)
async def create_account(
	company: Company, db: DB, account: pls.AccountCreate,
	account_data: sch.AccountInCreateUpdate
):
	return srv.create_account(db, company, account_data=account_data)


@account.post('/create-form/', 
	response_model=sch.AccountIn,
	status_code=status.HTTP_201_CREATED
)
async def create_account_form(
	company: Company, db: DB, ccount: pls.AccountCreate,
	bg_tasks: BackgroundTasks,
	form_data: frm.AccountFormData = Depends(),
	photo: UploadFile | None = None,
):
	profile_data = sch.ProfileInCreateUpdate(
		first_name = form_data.first_name,
		last_name = form_data.last_name,
		sex = form_data.sex,
		photo = None,
	)
	account_data = sch.AccountInCreateUpdate(
		email = form_data.email,
		username = form_data.username,
		is_valid = form_data.is_valid,
		password = form_data.password,
		profile = profile_data
	)
	return srv.create_account_form(db, company, bg_tasks, account_data=account_data, photo=photo)


@account.put('/{pk}/update/', 
	response_model=sch.AccountIn,
	status_code=status.HTTP_202_ACCEPTED
)
async def update_category( 
	company: Company, db: DB, account: pls.AccountUpdate,
	account_data: sch.AccountInCreateUpdate,
	pk: Annotated[int, Path(title="The ID account", gt=0)]
):
	return srv.update_account(db, company, account_id=pk, account_data=account_data)


@account.delete('/{pk}/delete/', 
	response_model=sch.AccountIn,
)
async def delete_account(
	company: Company, db: DB, account: pls.AccountDelete,
	pk: Annotated[int, Path(title="The ID account", gt=0)]
):
	srv.delete_account(db, company, account_id=pk)
	return Response(status_code=status.HTTP_204_NO_CONTENT)