from typing import Dict, List

from pydantic import BaseModel


class EcgParams(BaseModel):
    id: int
    images: Dict[str, str]
    amplitude: int
    write_speed: int


class AnnotationValue(BaseModel):
    x: float
    y: float
    width: float
    height: float
    rectanglelabels: List[str]
    rotation: int


class AnnotationResult(BaseModel):
    value: AnnotationValue
    original_height: int
    original_width: int
