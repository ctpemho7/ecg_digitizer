from http import HTTPStatus
from typing import Optional

import httpx


class DetectionClient:
    """
    Взаимодействие с сервисом для детекции отвдений ЭКГ.
    """

    def get_base_url(self) -> str:
        return "http://yolo-detector:8010/predict"

    def _request(self, endpoint: str) -> Optional[dict]:
        response = httpx.get(endpoint)
        if response.status_code == HTTPStatus.OK:
            return response.json()

        return None

    def get_predict(self, filename: str) -> Optional[list]:
        if response := self._request(f"{self.get_base_url()}?image={filename}"):
            return response
        return None
