from app.vendors.utils.gate import gate
from app.http.apps.auth import (
	Account,
	CurrentUser,
)
from fastapi import Depends
from typing import Annotated


async def get_current_category_for_show_list(account: CurrentUser):
	gate.allow(['show_category_list'], account)
	return account

CategoryShowList = Annotated[Account, Depends(get_current_category_for_show_list)]

async def get_current_category_for_show_item(account: CurrentUser):
	gate.allow(['show_category_item'], account)
	return account

CategoryShowItem = Annotated[Account, Depends(get_current_category_for_show_item)]

async def get_current_category_for_create(account: CurrentUser):
	gate.allow(['create_category'], account)
	return account

CategoryCreate = Annotated[Account, Depends(get_current_category_for_create)]

async def get_current_category_for_update(account: CurrentUser):
	gate.allow(['update_category'], account)
	return account

CategoryUpdate = Annotated[Account, Depends(get_current_category_for_update)]

async def get_current_category_for_delete(account: CurrentUser):
	gate.allow(['delete_category'], account)
	return account 

CategoryDelete = Annotated[Account, Depends(get_current_category_for_delete)]
