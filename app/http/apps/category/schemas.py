from pydantic import BaseModel
from datetime import datetime


class ParentCategoryOut(BaseModel):
	id: int
	name: dict
	
	class Config:
		orm_mode = True

class CategoryOut(BaseModel):
	id: int
	name: dict
	short_desc: dict
	created_at: datetime | None
	parent: ParentCategoryOut | None = None
	articles_count: int | None = None
	child_count: int | None = None

	class Config:
		orm_mode = True

