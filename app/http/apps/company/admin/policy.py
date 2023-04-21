from app.vendors.utils.gate import gate
from app.http.apps.auth import (
	Account,
	CurrentUser,
)
from fastapi import Depends
from typing import Annotated


async def get_current_account_for_show_list(account: CurrentUser):
	gate.allow(['show_company_list'], account)
	return account

CompanyShowList = Annotated[Account, Depends(get_current_account_for_show_list)]

async def get_current_account_for_show_item(account: CurrentUser):
	gate.allow(['show_company_item'], account)
	return account

CompanyShowItem = Annotated[Account, Depends(get_current_account_for_show_item)]

async def get_current_account_for_create(account: CurrentUser):
	gate.allow(['create_company'], account)
	return account

CompanyCreate = Annotated[Account, Depends(get_current_account_for_create)]

async def get_current_account_for_update(account: CurrentUser):
	gate.allow(['update_company'], account)
	return account

CompanyUpdate = Annotated[Account, Depends(get_current_account_for_update)]

async def get_current_account_for_delete(account: CurrentUser):
	gate.allow(['delete_company'], account)
	return account 

CompanyDelete = Annotated[Account, Depends(get_current_account_for_delete)]

