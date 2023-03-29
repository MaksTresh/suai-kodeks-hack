from celery import Celery

from config import get_settings, Settings


def create_celery_app(settings: Settings):
    return Celery(
        'celery',
        broker=f"amqp://{settings.RABBITMQ_USERNAME}:{settings.RABBITMQ_PASSWORD}"
               f"@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/",
        backend=f"redis://{settings.REDIS_USERNAME}:{settings.REDIS_PASSWORD}"
                f"@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB_NUMBER}/",
        include=settings.CELERY_IMPORTS,
        result_expires=settings.CELERY_RESULT_EXPIRES,
    )


celery_app = create_celery_app(get_settings())
