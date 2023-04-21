from pydantic import (
	BaseModel, 
	Field,
)


class CategoryInBase(BaseModel):
	slug: str = Field(
		title='Slug of the category', 
		max_length=180
	)
	name: dict
	short_desc: dict
	is_valid: bool
	parent_id: int | None = None
	
class CategoryIn(CategoryInBase):
	id: int 
	class Config:
		orm_mode = True

class CategoryInCreate(CategoryInBase):
	pass
	
class CategoryInUpdate(CategoryInBase):
	pass