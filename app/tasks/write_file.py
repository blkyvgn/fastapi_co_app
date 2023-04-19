import shutil 
from pathlib import Path
from fastapi import UploadFile
from app.config import cfg


def write_file(file: UploadFile, path: Path, chunk_size=cfg.chunk_size):
	file_path = path / file.filename
	try:
		with open(file_path, 'wb') as _fb:
			shutil.copyfileobj(file.file, _fb, chunk_size)
		return file_path
	except shutil.Error as e:
		# write error to log file
		return None