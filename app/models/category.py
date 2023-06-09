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
	JSON,
	Index,
	UniqueConstraint,
)


class Category(ValidMixin, TimestampsMixin, HelpersMixin, ImgUploadMixin, BaseModel):
	__tablename__ = 'categories'

	slug = Column(
		String(180), 
	)
	thumb = Column(
		String(300)
	)
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
	articles_count = Column(
		Integer,
	)
	child_count = Column(
		Integer,
	)


	__table_args__ = (
		Index("idx_category_slug_company", slug, company_id, unique=True),
		UniqueConstraint(slug, company_id, name='category_slug_company'),
	)

	@classmethod
	def with_parent(cls, db, rows):
		parent_ids = [i.parent_id for i in rows]

		select_parents = db.select(cls.id, cls.name).\
			filter_by(is_valid=True).filter(cls.id.in_(parent_ids))
		parents = db.session.execute(select_parents).all()

		res_items = []

		# for c in rows:
		# 	_parent = next((p for p in parents if c.parent_id == p.id), None)
		# 	_cat = shema.parse_obj(c._asdict())
		# 	if _parent:
		# 		_cat.parent = _parent
		# 	res_items.append(_cat)

		for c in rows:
			_parent = next((p for p in parents if c.parent_id == p.id), None)
			_c = c._asdict()
			_c['parent'] = _parent
			res_items.append(_c)

		return res_items

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

	

	# def __str__(self, level=0):
	# 	ret = f"{'    ' * level} {repr(self.name)} \n"
	# 	for child in self.children:
	# 		ret += child.__str__(level + 1)
	# 	return ret
