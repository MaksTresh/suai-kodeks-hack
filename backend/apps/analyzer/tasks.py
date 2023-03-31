import contextlib
import os
import sys

from PIL import Image

from apps.celery.celery_app import celery_app
from apps.analyzer.schemas import TaskResult
from yolov7.detect import predict
from config import get_settings


@celery_app.task(ignore_result=False)
def analyze_image(file_path: str) -> list[TaskResult]:
    """
    Essentially the run method of PredictTask
    """
    with contextlib.chdir("/app/yolov7"):
        sys.path.append("/app/yolov7")
        result = predict(file_path)

    image_path = result["image_path"]
    bboxes = result["result"]
    print(image_path)

    image = Image.open(file_path)
    result: list[dict] = []

    for i, box in enumerate(bboxes):
        cropped_image_name = f"{i}-{os.path.basename(image_path)}"
        x1, y1, x2, y2 = box['coords']
        cropped_image = image.crop(box=(x1, y1, x2, y2))
        cropped_image.save(os.path.join(get_settings().UPLOADED_IMAGES_DIR, cropped_image_name))

        result.append(TaskResult(table_img=cropped_image_name, type=box['label']).dict())

    return result
