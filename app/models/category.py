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


class Category(ValidMixin, TimestampsMixin, HelpersMixin, BaseModel):
	__tablename__ = 'categories'

	name = Column(
		JSON,
		default = dict
	)
	short_desc = Column(
		JSON,
		default = dict
	)
	parent_id = Column(
		Integer, 
		ForeignKey('categories.id'),
	)
	children = relationship(
		'Category', 
		backref=backref('parent', remote_side='Category.id')
	)
	articles = relationship(
		'Article', 
		back_populates='category'
	)
	company_id = Column(
		Integer, 
		ForeignKey('companies.id')
	)
	company = relationship(
		'Company', 
		back_populates='categories'
	)

	# def __str__(self, level=0):
	# 	ret = f"{'    ' * level} {repr(self.name)} \n"
	# 	for child in self.children:
	# 		ret += child.__str__(level + 1)
	# 	return ret
