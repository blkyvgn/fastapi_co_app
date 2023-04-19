from pydantic import BaseModel, Field
from app.config import cfg


class CompanyOutBase(BaseModel):
	alias: str = Field(
		default=cfg.company_alias, 
		title='Alias of the company', 
		max_length=30
	)
	name: dict
	options: dict
	articles_count: int | None = None

class CompanyOutItem(CompanyOutBase):
	id: int 
	class Config:
		orm_mode = True