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
)


class Company(ValidMixin, TimestampsMixin, HelpersMixin, ImgUploadMixin, BaseModel):
	__tablename__ = 'companies'

	alias = Column(
		String(30), 
		unique = True,
		index=True,
	)
	logo = Column(
		String(300)
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

	def upload_file(img_name, file: None, bg_task, img_width: int | None = None):
		img_field = getattr(self, image_name)
		if img_field and file:
			ext_img_path = f'images/company/{self.id}/logo'
			bg_task.add_task(self.save_and_resize_img, file, ext_img_path, img_width)
			self.img_field=f'{ext_img_path}/{file.filename}'