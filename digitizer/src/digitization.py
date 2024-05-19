import json
from typing import List, Dict

from integrations.aws import get_from_s3
from settings import settings
from schemas import AnnotationResult
from model.Lead import Lead, LeadId


def collect_leads(key):
    map_leads = {
        "I": LeadId.I,
        "II": LeadId.II,
        "III": LeadId.III,
        "aVF": LeadId.aVF,
        "aVL": LeadId.aVL,
        "aVR": LeadId.aVR,
        "V1": LeadId.V1,
        "V2": LeadId.V2,
        "V3": LeadId.V3,
        "V4": LeadId.V4,
        "V5": LeadId.V5,
        "V6": LeadId.V6,
    }

    def convert_lead(annotation: AnnotationResult) -> Lead:
        def calculate(percent: float, size: int) -> int:
            return int(percent * size / 100)

        value = annotation.value
        return Lead(
            x=calculate(value.x, annotation.original_width),
            y=calculate(value.y, annotation.original_height),
            width=calculate(value.width, annotation.original_width),
            height=calculate(value.height, annotation.original_height),
            startTime=0,
        )

    annotation_path = get_from_s3(key, settings.AWS_OUTPUT_BUCKET)
    with open(annotation_path, 'r') as f:
        annotation_json = json.load(f)

    annotations = []
    for result in annotation_json['result']:
        annotations.append(AnnotationResult(**result))

    leads = {
        map_leads[annotation.value.rectanglelabels[0]]: convert_lead(annotation)
        for annotation in annotations
    }

    return leads


def digitize_image(key):
    image_path = get_from_s3(key, settings.AWS_INPUT_BUCKET)


def to_wfdb():
    pass

