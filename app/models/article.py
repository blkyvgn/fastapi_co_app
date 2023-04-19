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
	Text,
	JSON,
)


class Article(ValidMixin, TimestampsMixin, HelpersMixin, BaseModel):
	__tablename__ = 'articles'

	category_id = Column(
		Integer, 
		ForeignKey('categories.id')
	)
	category = relationship(
		'Category', 
		back_populates='articles'
	)
	data = relationship(
		'ArticleData', 
		back_populates='article',
	)
	comments = relationship(
		'Comment', 
		back_populates='article'
	)
	account_id = Column(
		Integer, 
		ForeignKey('accounts.id')
	)
	account = relationship(
		'Account', 
		back_populates='articles'
	)
	company_id = Column(
		Integer, 
		ForeignKey('companies.id')
	)
	company = relationship(
		'Company', 
		back_populates='articles'
	)



class ArticleData(HelpersMixin, BaseModel):
	__tablename__ = 'articles_data'

	lang = Column(
		String(10), 
	) 
	name = Column(
		String(180),
	)
	short_desc = Column(
		String(400),
	)
	body = Column(
		Text, 
	)
	article_id = Column(
		Integer, 
		ForeignKey('articles.id'),
	)
	article = relationship(
		'Article', 
		back_populates='data',
	)


class Comment(TimestampsMixin, BaseModel):
	__tablename__ = 'comments'

	username = Column(
		String(120),
		nullable=False,
	) 
	text = Column(
		Text, 
	)
	article_id = Column(
		Integer, 
		ForeignKey('articles.id'),
	)
	article = relationship(
		'Article', 
		back_populates='comments',
	)