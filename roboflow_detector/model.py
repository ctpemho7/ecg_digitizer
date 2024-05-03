import logging
import os

import boto3
import json
from botocore.client import Config
from roboflow import Roboflow

from typing import List, Dict, Optional
from label_studio_ml.model import LabelStudioMLBase
from label_studio_sdk.objects import PredictionValue
from label_studio_ml.response import ModelResponse
from label_studio_sdk.label_interface.region import Region
from label_studio_ml.model import LabelStudioMLBase
from label_studio_ml.utils import (
    get_image_size,
    get_single_tag_keys,
    DATA_UNDEFINED_NAME,
)
from label_studio_tools.core.utils.io import get_data_dir, get_local_path
from botocore.exceptions import ClientError
from urllib.parse import urlparse

from schemas import RPredictionResponse, RImage, RPrediction

logger = logging.getLogger(__name__)


class NewModel(LabelStudioMLBase):
    """Custom ML Backend model
    """

    def __init__(self, **kwargs,):
        super().__init__(**kwargs)

        rf = Roboflow(api_key=os.getenv('ROBOFLOW_API_KEY'))
        project = rf.workspace().project("ecg-lead-classification")
        self.model = project.version(3).model

        params = get_single_tag_keys(
            self.parsed_label_config, "RectangleLabels", "Image"
        )
        self.from_name, self.to_name, self.value, self.labels_in_config = params

    def setup(self):
        """Configure any parameters of your model here
        """
        self.set("model_version", "0.0.1")

    def _get_image_url(self, task: Dict) -> str:
        image_url = task["data"].get("image") or task["data"].get(
            DATA_UNDEFINED_NAME
        )

        # retrieve image from s3 bucket,
        # set env vars AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
        # and AWS_SESSION_TOKEN to allow boto3 to access the bucket
        if image_url.startswith("s3://") and os.getenv('AWS_ACCESS_KEY_ID'):
            # pre-sign s3 url
            r = urlparse(image_url, allow_fragments=False)
            bucket_name = r.netloc
            key = r.path.lstrip("/")
            client = boto3.client("s3",
                                  endpoint_url='http://minio:9000',
                                  aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                                  config=Config(signature_version='s3v4'),
                                  region_name='us-west-rack-2'
                                  )
            try:
                image_url = client.generate_presigned_url(
                    ClientMethod="get_object",
                    Params={"Bucket": bucket_name, "Key": key},
                )
            except ClientError as exc:
                logger.warning(
                    f"Can't generate pre-signed URL for {image_url}. Reason: {exc}"
                )

        return image_url

    def predict(self, tasks: List[Dict], context: Optional[Dict] = None, **kwargs) -> ModelResponse:
        """ Write your inference logic here
            :param tasks: [Label Studio tasks in JSON format](https://labelstud.io/guide/task_format.html)
            :param context: [Label Studio context in JSON format](https://labelstud.io/guide/ml_create#Implement-prediction-logic)
            :return model_response
                ModelResponse(predictions=predictions) with
                predictions: [Predictions array in JSON format](https://labelstud.io/guide/export.html#Label-Studio-JSON-format-of-annotated-tasks)
        """
        print(f'''\
        Run prediction on {tasks}
        Received context: {context}
        Project ID: {self.project_id}
        Label config: {self.label_config}
        Parsed JSON Label config: {self.parsed_label_config}
        Extra params: {self.extra_params}''')

        predictions = []
        for task in tasks:
            image_url = self._get_image_url(task)
            print(f"image_url: {image_url}")
            image_path = get_local_path(image_url, task_id=task.get('id'))
            print(f"image_path: {image_url}")
            response = self.model.predict(image_path, confidence=30, overlap=50).json()
            from pprint import pprint
            pprint(response)

            rb_prediction = RPredictionResponse(
                predictions=[RPrediction(**p) for p in response['predictions']],
                image=RImage(**response['image'])
            )
            img_width, img_height = rb_prediction.image.width, rb_prediction.image.height

            results = []
            all_scores = []
            for prediction in rb_prediction.predictions:
                results.append(
                    {
                        "from_name": self.from_name,
                        "to_name": self.to_name,
                        "type": "rectanglelabels",
                        "value": {
                            "rectanglelabels": [prediction.class_name],
                            "x": float(prediction.x) / img_width * 100,
                            "y": float(prediction.y) / img_height * 100,
                            "width": float(prediction.width) / img_width * 100,
                            "height": float(prediction.height) / img_height * 100,
                        },
                        "score": prediction.confidence,
                    }
                )
                all_scores.append(prediction.confidence)

            print(results)
            avg_score = sum(all_scores) / max(len(all_scores), 1)
            predictions.append(
                PredictionValue(
                    model_version=self.get("model_version"),
                    score=avg_score,
                    result=results
                )
            )
            print(predictions)
        # example for resource downloading from Label Studio instance,
        # you need to set env vars LABEL_STUDIO_URL and LABEL_STUDIO_API_KEY
        # path = self.get_local_path(tasks[0]['data']['image_url'], task_id=tasks[0]['id'])

        # example for simple classification
        # return [{
        #     "model_version": self.get("model_version"),
        #     "score": 0.12,
        #     "result": [{
        #         "id": "vgzE336-a8",
        #         "from_name": "sentiment",
        #         "to_name": "text",
        #         "type": "choices",
        #         "value": {
        #             "choices": [ "Negative" ]
        #         }
        #     }]
        # }]

        return ModelResponse(predictions=predictions)

    def fit(self, event, data, **kwargs):
        """
        This method is called each time an annotation is created or updated
        You can run your logic here to update the model and persist it to the cache
        It is not recommended to perform long-running operations here, as it will block the main thread
        Instead, consider running a separate process or a thread (like RQ worker) to perform the training
        :param event: event type can be ('ANNOTATION_CREATED', 'ANNOTATION_UPDATED')
        :param data: the payload received from the event (check [Webhook event reference](https://labelstud.io/guide/webhook_reference.html))
        """

        # use cache to retrieve the data from the previous fit() runs
        old_data = self.get('my_data')
        old_model_version = self.get('model_version')
        print(f'Old data: {old_data}')
        print(f'Old model version: {old_model_version}')

        # store new data to the cache
        self.set('my_data', 'my_new_data_value')
        self.set('model_version', 'my_new_model_version')
        print(f'New data: {self.get("my_data")}')
        print(f'New model version: {self.get("model_version")}')

        print('fit() completed successfully.')
