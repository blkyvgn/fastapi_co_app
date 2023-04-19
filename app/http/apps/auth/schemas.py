from datetime import date 
from decimal import Decimal
from enum import Enum
from pydantic import (
	BaseModel, 
	ValidationError, 
	validator,
)
# from fastapi import (
# 	HTTPException,
# 	status,
# )
from app.vendors.helpers.validators import (
	email_validation_check,
	passwd_validation_check,
)


class ProfileInBase(BaseModel):
	first_name: str
	last_name: str
	female: bool

class ProfileIn(ProfileInBase):
	id: int 
	class Config:
		orm_mode = True

class ProfileInCreate(ProfileInBase):
	pass 


class AccountBase(BaseModel):
	email: str 
	username: str
	is_valid: bool = False
	is_activated: bool = False
	permissions: list[str] = []

	@validator('email')
	def email_validation(cls, v):
		if not email_validation_check(v):
			raise ValueError('not valid email')
		return v

	@validator('username')
	def username_alphanumeric(cls, v):
		assert v.isalnum(), 'must be alphanumeric'
		return v

	
class Account(AccountBase):
	id: int 

	# def gate(self, key: str,  permissions: list[str] = []): # account.gate('allow', ['access_admin'])
	# 	''' permission. key: allow or deny, 
	# 	allow - if all from list of permissions, 
	# 	deny - if one from list of permissions '''
	# 	if key == 'allow':
	# 		if not frozenset(self.permissions) <= frozenset(permissions):
	# 			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
	# 	else: # deny
	# 		if not len(frozenset(self.permissions) & frozenset(permissions)) == 0:
	# 			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

	class Config:
		orm_mode = True



class AccountCreate(AccountBase):
	password: str
	password_confirmation: str

	profile: ProfileInCreate

	@validator('password')
	def password_validation(cls, v):
		if not passwd_validation_check(v):
			raise ValueError('not valid password')
		return v

	@validator('password_confirmation')
	def passwords_match(cls, v, values, **kwargs):
		if 'password' in values and v != values['password']:
			raise ValueError('passwords do not match')
		return v

class Token(BaseModel):
	access_token: str
	token_type: str = 'bearer'

class AccountEmail(BaseModel):
	email: str

	@validator('email')
	def email_validation(cls, v):
		if not email_validation_check(v):
			raise ValueError('not valid email')
		return v

class ResetPassword(BaseModel):
	password: str
	password_confirmation: str

	@validator('password')
	def password_validation(cls, v):
		if not passwd_validation_check(v):
			raise ValueError('not valid password')
		return v

	@validator('password_confirmation')
	def passwords_match(cls, v, values, **kwargs):
		if 'password' in values and v != values['password']:
			raise ValueError('passwords do not match')
		return v