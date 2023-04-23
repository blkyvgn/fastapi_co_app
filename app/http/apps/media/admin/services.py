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



async def async_upload_video(db: DB, company: Company, pk: int, file: None):
	media = mdl.Media.get_first_item_by_filter(db, id=pk, is_valid=True)
	if media is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Media not found'
		) from None
	# try:
	ext_img_path = f'images/media/{pk}/video'
	video_path = media.save_video(file, ext_img_path)
	print('-----------------------------------------------------')
	print(video_path)
	print('-----------------------------------------------------')
	# file_path = None
	media.file = video_path
	# media.file_type = 'video'
	db.session.add(media)
	db.session.commit()
	return {'success': f'File uploaded (Media:{pk})'}
	# except:
		# return {'error':'error'}