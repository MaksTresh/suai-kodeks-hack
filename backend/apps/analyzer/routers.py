from pathlib import Path
from typing import Any
from uuid import uuid4

from celery.result import AsyncResult
from fastapi import APIRouter, Depends, UploadFile
from pydantic import parse_obj_as
from starlette.requests import Request
from starlette.responses import FileResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from apps.analyzer.dependencies import valid_file_name, valid_image
from apps.analyzer.schemas import TaskResult, TaskSchema, TaskStatus
from apps.analyzer.tasks import analyze_image
from apps.analyzer.utils import save_file
from config import Settings, get_settings

router = APIRouter()


@router.post(
    "/tasks",
    response_model=TaskSchema,
    status_code=HTTP_201_CREATED,
    response_description="Создание задачи на анализ изображения",
)
async def predict(
    request: Request,
    image: UploadFile = Depends(valid_image),
    settings: Settings = Depends(get_settings),
) -> TaskSchema:
    file_name = f"{uuid4().hex}{Path(image.filename).suffix}"
    file_path = await save_file(image, file_name, settings)

    task = analyze_image.delay(file_path)
    return TaskSchema(
        task_id=str(task),
        status=TaskStatus.PENDING,
    )


@router.get(
    "/tasks/result_image",
    response_class=FileResponse,
    status_code=HTTP_200_OK,
    response_description="Получение изображения",
)
async def get_result_file(
    request: Request,
    file_path: str = Depends(valid_file_name),
) -> FileResponse:
    return FileResponse(file_path)


@router.get(
    "/tasks/{task_id}",
    status_code=HTTP_200_OK,
    response_model=TaskSchema,
    response_description="Получение статуса задачи по анализу изображения",
)
async def get_result_status(
    request: Request,
    task_id: str,
) -> Any:
    task = AsyncResult(task_id)
    if not task.ready():
        return TaskSchema(
            task_id=task_id,
            status=TaskStatus.PENDING,
        )

    print(task.result)

    return TaskSchema(
        task_id=task_id,
        status=TaskStatus.SUCCESS,
        result=parse_obj_as(list[TaskResult], task.result),
    )