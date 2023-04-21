from pydantic import BaseModel, Field
from enum import Enum
from typing import Any



class CategoryOut(BaseModel):
	id: int 
	slug: str
	name: dict
	class Config:
		orm_mode = True

class AccountOut(BaseModel):
	id: int 
	username: str
	class Config:
		orm_mode = True

class ArticleOutData(BaseModel):
	id: int
	lang: str
	name: str
	short_desc: str
	body: str
	class Config:
		orm_mode = True

class ArticleOut(BaseModel):
	id: int
	slug: str 
	category: CategoryOut
	account: AccountOut
	data: list[ArticleOutData] = []

	class Config:
		orm_mode = True
