from dataclasses import dataclass
from pydantic import EmailStr
from typing import Annotated
from fastapi import Form
from app.models.account import SexEnum


@dataclass
class AccountFormData:
	first_name: Annotated[str, Form(...)]
	last_name: Annotated[str, Form(...)]
	sex: Annotated[SexEnum, Form(...)]
	email: Annotated[EmailStr, Form(...)]
	username: Annotated[str, Form(...)]
	is_valid: Annotated[bool, Form(...)]
	password: Annotated[str, Form(...)]