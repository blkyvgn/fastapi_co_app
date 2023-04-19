import aiofiles
from fastapi import UploadFile


async def write_video(file_name: str, file: UploadFile):
	async with aiofiles.open(file_name, "wb") as buffer:
		data = await file.read()
		await buffer.write(data)
