import importlib
from abc import ABC

from celery import Task
from apps.celery.celery_app import celery_app


class PredictTask(Task, ABC):
    abstract = True

    def __init__(self):
        super().__init__()
        self.model = None

    def __call__(self, *args, **kwargs):
        if not self.model:
            module_import = importlib.import_module(self.path[0])
            model_obj = getattr(module_import, self.path[1])
            self.model = model_obj()
        return self.run(*args, **kwargs)


@celery_app.task(
    ignore_result=False,
    bind=True,
    base=PredictTask,
    path=('apps.analyzer.analyzer_model', 'AnalyzerModel'),
    name='{}.{}'.format(__name__, 'AnalyzerModel')
)
def analyze_image(self, file_path: str):
    """
    Essentially the run method of PredictTask
    """
    prediction = self.model.predict(file_path)
    return prediction
