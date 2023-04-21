from app.vendors.utils.gate import gate
from app.http.apps.auth import (
	Account,
	CurrentUser,
)
from fastapi import Depends
from typing import Annotated


async def get_current_account_for_show_list(account: CurrentUser):
	gate.allow(['show_account_list'], account)
	return account

AccountShowList = Annotated[Account, Depends(get_current_account_for_show_list)]

async def get_current_account_for_show_item(account: CurrentUser):
	gate.allow(['show_account_item'], account)
	return account

AccountShowItem = Annotated[Account, Depends(get_current_account_for_show_item)]

async def get_current_account_for_create(account: CurrentUser):
	gate.allow(['create_account'], account)
	return account

AccountCreate = Annotated[Account, Depends(get_current_account_for_create)]

async def get_current_account_for_update(account: CurrentUser):
	gate.allow(['update_account'], account)
	return account

AccountUpdate = Annotated[Account, Depends(get_current_account_for_update)]

async def get_current_account_for_delete(account: CurrentUser):
	gate.allow(['delete_account'], account)
	return account 

AccountDelete = Annotated[Account, Depends(get_current_account_for_delete)]
