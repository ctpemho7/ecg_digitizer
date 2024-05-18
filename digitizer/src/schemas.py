from typing import Dict

from pydantic import BaseModel


class EcgParams(BaseModel):
    images: Dict[str, str]
    amplitude: int
    write_speed: int
