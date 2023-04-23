from app.vendors.base.database import BaseModel
from sqlalchemy.orm import (
	relationship,
	backref,
)
from app.vendors.mixins.model import (
	TimestampsMixin, 
	ValidMixin,
	HelpersMixin,
	ImgUploadMixin,
)
from sqlalchemy import (
	Column, 
	ForeignKey, 
	Integer, 
	String,
	Text,
	JSON,
	Index,
	UniqueConstraint,
)


class Article(ValidMixin, TimestampsMixin, HelpersMixin, ImgUploadMixin, BaseModel):
	__tablename__ = 'articles'

	slug = Column(
		String(180),
	)
	thumb = Column(
		String(300)
	)
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

	__table_args__ = (
		Index("idx_article_slug_company", slug, company_id, unique=True),
		UniqueConstraint(slug, company_id, name='article_slug_company'),
	)

	def upload_file(self, image_name, file: None, img_width: int | None = None):
		if hasattr(self, image_name) and file:
			ext_img_path = f'images/{self.__class__.__name__.lower()}/{self.id}/{image_name}'
			img_path = self.save_and_resize_img(file, ext_img_path, img_width)
			setattr(self, image_name, img_path)
		return img_path

	async def async_upload_file(self, image_name, file: None, img_width: int | None = None):
		img_path = None
		if hasattr(self, image_name) and file:
			ext_img_path = f'images/{self.__class__.__name__.lower()}/{self.id}/{image_name}'
			img_path = self.save_and_resize_img(file, ext_img_path, 60)
		return img_path



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