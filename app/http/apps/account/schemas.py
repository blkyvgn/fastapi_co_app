from pydantic import (
	BaseModel,
	Field,
	EmailStr
)
from enum import Enum
from typing import Any
from app.models.account import SexEnum

class Photo(BaseModel):
	url: str | None = None  # HttpUrl
	name: str | None = None

# class SexEnum(str, Enum):
# 	male = 'male'
# 	female = 'female'

class AccountOutBase(BaseModel):
	first_name: str = Field(..., 
		title='First name', description='User first name',
		min_length=4, max_length=80)
	last_name: str = Field(..., 
		title='Last name', description='User last name',
		min_length=4, max_length=80)
	email: EmailStr
	username: str = Field(..., 
		title='user name (login)', description='User login',
		min_length=3, max_length=30)
	sex: SexEnum = SexEnum.female
	articles_count: int | None = None

	photo: Photo | str | None = None


class AccountOut(AccountOutBase):
	id: int

	class Config:
		orm_mode = True
