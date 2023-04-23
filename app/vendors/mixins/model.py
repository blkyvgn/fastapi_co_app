from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import declarative_mixin
from datetime import timezone
from app.vendors.helpers.image import (
    resize_image, 
    async_resize_image,
)
from sqlalchemy import (
    func, 
    or_,
)
from sqlalchemy import (
	Column, 
	DateTime,
    Boolean,
)
from app.vendors.helpers.file import (
    write_file, 
    async_write_file,
    get_or_create_storage_dir,
)
import aiofiles
from pathlib import Path
from app.config import cfg



@declarative_mixin
class TimestampsMixin:
    created_at = Column(
    	DateTime, 
    	default=func.now()
    )
    updated_at = Column(
    	DateTime, 
    	nullable=True,
    )
    # updated_at = Column(
    #     DateTime(timezone=True), 
    #     server_default=func.now(), 
    #     onupdate=func.now()
    # )


@declarative_mixin
class ValidMixin:
    is_valid = Column(
        Boolean,
        default=True,
    )

class HelpersMixin:
    @classmethod
    def get_first_item_by_filter(cls, db, _or=False, **kwargs):
        if not _or:
            item_select = db.select(cls).filter_by(**kwargs)
        else:
            filters = [getattr(cls, k) == v for k, v in kwargs.items()]
            item_select = db.select(cls).filter(or_(False, *filters))
        item = db.session.execute(item_select).scalar()
        return item

class ImgUploadMixin:

    async def async_save_and_resize_img(self, img, ext_path: str, img_width: int | None):
        if not img:
            return None
        try:
            storage_path = cfg.root_path / cfg.upload_folder_dir
            dir_path = get_or_create_storage_dir(storage_path, ext_path)
            img_file_path = await async_write_file(img, dir_path)
            if img_width:
               res = await async_resize_image(img_file_path, img_width)
            img_file_path = f'{ext_path}/{img.filename}'
        except:
            img_file_path = None

        return img_file_path


    def save_and_resize_img(self, img, ext_path: str, img_width: int | None):
        if not img:
            return None
        try:
            storage_path = cfg.root_path / cfg.upload_folder_dir
            dir_path = get_or_create_storage_dir(storage_path, ext_path)
            img_file_path = write_file(img, dir_path)
            if img_width:
                resize_image(img_file_path, img_width)
            img_file_path = f'{ext_path}/{img.filename}'
        except:
            img_file_path = None

        return img_file_path



    

            


