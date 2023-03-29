from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class IncorrectImageException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Файл не является картинкой!",
        )


class IncorrectFileName(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Такого файла не существует!",
        )
