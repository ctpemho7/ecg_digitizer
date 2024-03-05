from fastapi import FastAPI
from roboflow import Roboflow
from settings import settings


app_params = {
    "debug": settings.debug,
    "title": f'API системы "{settings.project.title}"',
    "description": settings.project.description,
    "version": settings.project.release_version,
}
app = FastAPI(**app_params)
rf = Roboflow(api_key=settings.roboflow_api_key)


@app.get("/predict")
def hello_world(image: str):
    project = rf.workspace().project("ecg-lead-classification")
    model = project.version(3).model

    path = f"/media/{image}"
    result = model.predict(path, confidence=30, overlap=50).json()

    print(result)
    return result
