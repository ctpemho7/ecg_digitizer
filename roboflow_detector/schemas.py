from typing import List, Dict, Any
from pydantic import BaseModel, Field

#
# Для Roboflow
#


class RPrediction(BaseModel):
    x: int
    y: int
    width: int
    height: int
    confidence: float
    class_name: str = Field(..., alias="class")
    class_id: int
    detection_id: str
    image_path: str
    prediction_type: str


class RImage(BaseModel):
    width: int
    height: int


class RPredictionResponse(BaseModel):
    predictions: List[RPrediction]
    image: RImage


#
# Для Label Studio
#
class LSValue(BaseModel):
    x: float
    y: float
    width: float
    height: float
    rectanglelabels: List[str]
    rotation: int


class LSResult(BaseModel):
    from_name: str
    to_name: str
    type: str
    value: LSValue
    score: float


class LSPredictionOneTask(BaseModel):
    result: List[LSResult]
    score: float
    model_version: float
