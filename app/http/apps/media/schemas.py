from pydantic import BaseModel, Field
from enum import Enum
from typing import Any
from app.models.media import MediaTypeEnum


class AccountOut(BaseModel):
	id: int 
	username: str
	class Config:
		orm_mode = True

class MediaOut(BaseModel):
	id: int
	slug: str 
	name: dict
	short_desc: dict
	file_type: MediaTypeEnum = MediaTypeEnum.video
	file: str
	account: AccountOut

	class Config:
		orm_mode = True