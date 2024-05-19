from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse

from settings import settings
from schemas import EcgParams

app_params = {
    "debug": settings.debug,
    "title": f'API системы "{settings.project.title}"',
    "description": settings.project.description,
    "version": settings.project.release_version,
}
app = FastAPI(**app_params)


@app.post("/digitize")
def hello_world(params: EcgParams):
    from pprint import pprint
    pprint(params.dict())
    print(params.write_speed)
    import time
    time.sleep(10)
    data = {"message": "ECG DIGITIZED"}
    return JSONResponse(content=data, status_code=201)
