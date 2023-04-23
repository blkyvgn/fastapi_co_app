from app.vendors.dependencies import DB, Company
from app.vendors.helpers.video import write_video
# from app.vendors.helpers.file import (
# 	get_or_create_storage_dir,
# )
from starlette.requests import Request
from typing import IO, Generator
from pathlib import Path
from uuid import uuid4
import aiofiles
from fastapi import (
	UploadFile, 
	BackgroundTasks, 
	HTTPException, 
)
import shutil
from app import models as mdl
from app.config import cfg


def ranged(
		file: IO[bytes],
		start: int = 0,
		end: int = None,
		block_size: int = cfg.block_size,
) -> Generator[bytes, None, None]:
	consumed = 0

	file.seek(start)
	while True:
		data_length = min(block_size, end - start - consumed) if end else block_size
		if data_length <= 0:
			break
		data = file.read(data_length)
		if not data:
			break
		consumed += data_length
		yield data

	if hasattr(file, 'close'):
		file.close()


async def open_file(request: Request, db: DB, video_pk: int) -> tuple:
	media = await mdl.Media.get(db, id=video_pk)
	file = media.file
	if file is None:
		raise HTTPException(status_code=404, detail="Not found")
	# path = Path(file.dict().get('file'))
	# path = Path(file.file)
	path = cfg.root_path / cfg.upload_folder_dir / file
	# path = Path(file)
	file = path.open('rb')
	file_size = path.stat().st_size

	content_length = file_size
	status_code = 200
	headers = {}
	content_range = request.headers.get('range')

	if content_range is not None:
		content_range = content_range.strip().lower()
		content_ranges = content_range.split('=')[-1]
		range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
		range_start = max(0, int(range_start)) if range_start else 0
		range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
		content_length = (range_end - range_start) + 1
		file = ranged(file, start=range_start, end=range_end + 1)
		status_code = 206
		headers['Content-Range'] = f'bytes {range_start}-{range_end}/{file_size}'

	return file, status_code, content_length, headers