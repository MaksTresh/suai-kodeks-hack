import os

import aiofiles
from starlette.datastructures import UploadFile

from config import Settings


async def save_file(file: UploadFile, filename: str, settings: Settings) -> str:
    await file.seek(0)
    file_path = os.path.join(settings.UPLOADED_IMAGES_DIR, filename)

    async with aiofiles.open(file_path, "wb") as f:
        while content := await file.read(1024):
            await f.write(content)

    return file_path
