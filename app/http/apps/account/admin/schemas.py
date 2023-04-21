from pydantic import (
	BaseModel,
	Field,
	EmailStr,
	ValidationError, 
	validator,
)
from enum import Enum
from typing import Any
from app.models.account import SexEnum
from app.vendors.helpers.validators import (
	email_validation_check,
	passwd_validation_check,
)

class Photo(BaseModel):
	url: str | None = None  # HttpUrl
	name: str | None = None

class ProfileInBase(BaseModel):
	first_name: str = Field(..., 
		title='First name', description='User first name',
		min_length=4, max_length=80)
	last_name: str = Field(..., 
		title='Last name', description='User last name',
		min_length=4, max_length=80)
	photo: Photo | str | None = None
	sex: SexEnum = SexEnum.female

class ProfileIn(ProfileInBase):
	class Config:
		orm_mode = True

class ProfileInCreateUpdate(ProfileInBase):
	pass


class AccountInBase(BaseModel):
	email: EmailStr
	username: str = Field(..., 
		title='user name (login)', description='User login',
		min_length=3, max_length=30
	)
	is_valid: bool = False
	is_activated: bool = False

	profile: ProfileIn | None = None


class AccountIn(AccountInBase):
	id: int | None

	class Config:
		orm_mode = True

class AccountInCreateUpdate(AccountInBase):
	password: str = Field(...,
		title='User password', description='User password',
		min_length=8, max_length=16
	)

	@validator('email')
	def email_validation(cls, v):
		if not email_validation_check(v):
			raise ValueError('not valid email')
		return v

	@validator('username')
	def username_alphanumeric(cls, v):
		assert v.isalnum(), 'must be alphanumeric'
		return v

	@validator('password')
	def password_validation(cls, v):
		if not passwd_validation_check(v):
			raise ValueError('not valid password')
		return v