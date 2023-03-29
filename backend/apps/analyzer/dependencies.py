import os

import aiofiles
from PIL import Image
from fastapi import UploadFile, Depends
from pathvalidate import sanitize_filename

from apps.analyzer.exceptions import IncorrectImageException, IncorrectFileName
from config import get_settings, Settings


async def valid_image(file: UploadFile) -> UploadFile:
    try:
        img = Image.open(file.file)
        img.verify()
    except Exception:
        raise IncorrectImageException()

    return file


async def valid_file_name(file_name: str, settings: Settings = Depends(get_settings)) -> str:
    file_name = sanitize_filename(file_name)
    file_path = os.path.join(settings.UPLOADED_IMAGES_DIR, file_name)

    try:
        await aiofiles.open(file_path)
    except FileNotFoundError:
        raise IncorrectFileName()

    return file_path
