from pathlib import Path
from app.config import cfg
from datetime import datetime


def write_to_log(username: str, log_message='', level=None):
	log_file_path = cfg.root_path / cfg.log_dir
	log_file = log_file_path / 'log.txt'
	with open(log_file, mode='a') as log_file:
		content = f'{username}:\t{log_message}:\t{datetime.now()}\n'
		log_file.write(content)