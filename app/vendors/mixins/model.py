from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import declarative_mixin
from app.vendors.helpers.image import resize_image
from datetime import timezone
from sqlalchemy import (
    func, 
    or_,
)
from sqlalchemy import (
	Column, 
	DateTime,
    Boolean,
)
# import aiofiles
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


    

            


