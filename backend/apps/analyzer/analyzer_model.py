from apps.yolov7 import detect


class AnalyzerModel:
    def __init__(self):
        pass

    def predict(self, image: str):
        detect(image)
        return image
