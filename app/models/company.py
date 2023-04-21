from app.vendors.base.database import BaseModel
from sqlalchemy.orm import (
	relationship,
	backref,
)
from app.vendors.mixins.model import (
	TimestampsMixin, 
	ValidMixin,
	HelpersMixin,
)
from sqlalchemy import (
	Column, 
	ForeignKey, 
	Integer, 
	String,
	JSON,
)


class Company(ValidMixin, TimestampsMixin, HelpersMixin, BaseModel):
	__tablename__ = 'companies'

	alias = Column(
		String(30), 
		unique = True,
		index=True,
	)
	name = Column(
		JSON,
		default = dict
	)
	options = Column(
		JSON,
		default = dict
	)
	articles = relationship(
		'Article', 
		back_populates='company'
	)
	categories = relationship(
		'Category', 
		back_populates='company'
	)
	media = relationship(
		'Media', 
		back_populates='company'
	)
	chat_rooms = relationship(
		'Room', 
		back_populates='company'
	)
	roles = relationship(
		'Role', 
		back_populates='company'
	)