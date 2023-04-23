from app.vendors.dependencies import DB, Company
from sqlalchemy.orm.exc import NoResultFound
from fastapi import (
	HTTPException,
	status,
)
from enum import Enum
from sqlalchemy import desc
from app import models as mdl
from . import schemas as sch
from app.config import cfg



class FileWidth(int, Enum):
	thumbnail = cfg.image_width['THUMBNAIL']
	showcase  = cfg.image_width['SHOWCASE']
	slider    = cfg.image_width['SLIDER']
	logo      = cfg.image_width['LOGO']

async def async_upload_thumb(db: DB, company: Company, pk: int, file: None, width: int):
	article = mdl.Article.get_first_item_by_filter(db, id=pk, is_valid=True)
	if article is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Article not found'
		) from None
	try:
		ext_img_path = f'images/article/{pk}/thumb'
		img_path = article.save_and_resize_img(file, ext_img_path, width)
		file_path = None
		article.thumb = img_path
		db.session.add(article)
		db.session.commit()
		return {'success': f'File uploaded (Article:{pk})'}
	except:
		return {'error':'error'}