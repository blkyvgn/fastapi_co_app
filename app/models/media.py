from app.vendors.base.database import BaseModel
from app.vendors.helpers.image import resize_image
from app.vendors.helpers.file import (
	write_file, 
	get_or_create_storage_dir,
)
from sqlalchemy.orm import (
	relationship,
	backref,
)
from app.vendors.mixins.model import (
	TimestampsMixin, 
	ValidMixin,
	HelpersMixin,
)
import enum
from sqlalchemy import (
	Column, 
	ForeignKey, 
	Integer, 
	String,
	Text,
	JSON,
	Enum,
	Index,
	UniqueConstraint,
)

class MediaTypeEnum(enum.Enum):
    image = 'image'
    video = 'video'
    audio = 'audio'

class Media(ValidMixin, TimestampsMixin, HelpersMixin, BaseModel):
	__tablename__ = 'medias'

	slug = Column(
		String(180),
	)
	name = Column(
		JSON,
		default = dict
	)
	short_desc = Column(
		JSON,
		default = dict
	)
	file_type = Column(
		Enum(MediaTypeEnum)
	)
	file = Column(
		String(1000),
	)
	account_id = Column(
		Integer, 
		ForeignKey('accounts.id')
	)
	account = relationship(
		'Account', 
		back_populates='media'
	)
	company_id = Column(
		Integer, 
		ForeignKey('companies.id')
	)
	company = relationship(
		'Company', 
		back_populates='media'
	)
	__table_args__ = (
		Index("idx_media_slug_company", slug, company_id, unique=True),
		UniqueConstraint(slug, company_id, name='media_slug_company'),
	)

	@classmethod
	async def get(cls, db, **kwargs):
		return cls.get_first_item_by_filter(db, id=kwargs.get('id', None))

	@classmethod
	async def create(cls, db, **kwargs):
		new_item = cls(**kwargs)
		db.session.add(new_item)
		db.session.commit()
		db.session.refresh(new_item)
		return new_item

	@staticmethod
	def save_and_resize_img(img, ext_path: str, img_width: int | None = None):
		if not img:
			return None
		try:
			storage_path = cfg.root_path / cfg.upload_folder_dir
			dir_path = get_or_create_storage_dir(storage_path, ext_path)
			photo_file_path = write_file(img, dir_path)
			if img_width:
				resize_image(photo_file_path, img_width)
			photo_file_subpath = f'{ext_path}/{img.filename}'
		except:
			photo_file_subpath = None

		return photo_file_subpath

