import aiofiles
import shutil 
from pathlib import Path
from fastapi import (
	HTTPException,
	status,
	UploadFile
)
from app.config import cfg


async def aio_write_file(file: UploadFile, path: Path, chunk_size=cfg.chunk_size):
	file_path = path / file.filename
	async with aiofiles.open(file_path, 'wb') as _fb:
		while True:
			chunk = await file.read(chunk_size)
			if not chunk:
				break
			await _fb.write(chunk)
		return file.filename
	return None


async def async_write_file(file: UploadFile, path: Path, chunk_size=cfg.chunk_size):
	file_path = path / file.filename
	async with open(file_path, 'wb') as _fb:
		await shutil.copyfileobj(file.file, _fb, chunk_size)
	return file.filename


def write_file(file: UploadFile, path: Path, chunk_size=cfg.chunk_size):
	file_path = path / file.filename
	with open(file_path, 'wb') as _fb:
		shutil.copyfileobj(file.file, _fb, chunk_size)
	return file_path


def get_or_create_storage_dir(storage_path: Path, ext_path: str):
	dir_path = storage_path / ext_path
	try:
		dir_path.mkdir(parents=True, exist_ok=True)
		return dir_path
	except:
		return
