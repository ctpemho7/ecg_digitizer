from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse

from digitization import digitize_ecg
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
def digitizing(params: EcgParams):
    print("Запрос на оцифровку")
    from pprint import pprint
    pprint(params.dict())
    header, signal = digitize_ecg(params)
    data = {
        "message": "ECG DIGITIZED",
        "result": {
            "header": header,
            "signal": signal
        },
    }

    return JSONResponse(content=data, status_code=201)
