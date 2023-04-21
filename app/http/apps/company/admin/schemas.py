from pydantic import (
	BaseModel, 
	Field,
)
from app.config import cfg


class CompanyInBase(BaseModel):
	alias: str = Field(
		default=cfg.company_alias, 
		title='Alias of the company', 
		max_length=30
	)
	name: dict
	options: dict
	is_valid: bool
	
class CompanyIn(CompanyInBase):
	id: int 
	class Config:
		orm_mode = True

class CompanyInCreate(CompanyInBase):
	pass
	
class CompanyInUpdate(CompanyInBase):
	pass