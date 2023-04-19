from sqlalchemy.orm import relationship
from app.vendors.base.database import BaseModel
from sqlalchemy import (
	Column, 
	ForeignKey, 
	Integer, 
	String,
)


class TagItem(BaseModel):
	__tablename__ = 'tag_items'

	name = Column(
		String, 
		unique=True,
	)


class Tag(BaseModel):
	__tablename__ = 'tags'

	tag_id = Column(
		Integer, 
	)
	item_key = Column(
		String(50), 
	) 
	item_id = Column(
		Integer, 
	)