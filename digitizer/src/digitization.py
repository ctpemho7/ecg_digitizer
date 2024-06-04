import json
from pprint import pprint

import cv2
from pathlib import Path

import numpy as np
import wfdb
from matplotlib import pyplot as plt

from enter import convertECGLeads
from integrations.aws import get_from_s3, save_ecg_to_s3
from model.InputParameters import InputParameters
from settings import settings
from schemas import AnnotationResult, EcgParams
from model.Lead import Lead, LeadId
from ecgdigitize.image import openImage


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


def digitize_image(image, annotation, write_speed, amplitude):
    # получить изображение
    image_path = get_from_s3(image, settings.AWS_INPUT_BUCKET)
    # получить аннотации в нужном формате для алгоритма
    leads = collect_leads(annotation)

    params = InputParameters(
        rotation=0,
        timeScale=write_speed,
        voltScale=amplitude,
        leads=leads
    )
    image_path = Path(image_path)
    image_path = openImage(image_path)
    extracted_signals, preview_images = convertECGLeads(image_path, params)
    return extracted_signals


def to_wfdb(extracted_signals, name) -> tuple[str, str]:
    # сохранить в хранилище и вернуть пути

    # занулить NaN
    for lead in extracted_signals:
        extracted_signals[lead] = np.nan_to_num(extracted_signals[lead])

    # определить порядок
    signal_order = [LeadId.I, LeadId.II, LeadId.III, LeadId.aVR, LeadId.aVL, LeadId.aVF, LeadId.V1, LeadId.V2,
                    LeadId.V3, LeadId.V4, LeadId.V5, LeadId.V6]
    # signals = np.array([extracted_signals[lead] for lead in signal_order])
    # без транспонирования не работает
    # signals = signals.T

    max_length = max(len(extracted_signals[lead]) for lead in extracted_signals)
    signals = np.zeros((max_length, len(extracted_signals)))

    for i, lead in enumerate(signal_order):
        signals[:len(extracted_signals[lead]), i] = extracted_signals[lead]

    record_name = f'wfdb_{name}'
    local_dir_name = '/tmp'
    wfdb.wrsamp(record_name=record_name, fs=500, units=['mV'] * len(signal_order),
                sig_name=[repr(lead) for lead in signal_order], p_signal=signals,
                write_dir=local_dir_name)
    header_path = f"{local_dir_name}/{record_name}.hea"
    signal_path = f"{local_dir_name}/{record_name}.dat"
    print(f"Запись сохранена как {header_path} и {signal_path}")

    return header_path, signal_path


def digitize_ecg(params: EcgParams) -> tuple[str, str]:
    # оцифровка для каждого изображения
    signals = dict()
    for image_path, annotation_path in params.images.items():
        signals.update(digitize_image(image_path, annotation_path, params.write_speed, params.amplitude))
    print("signals")
    pprint(signals)

    # записать в wfdb, получить пути локально
    header, signal = to_wfdb(signals, params.id)

    # сохранить в хранилище и вернуть пути в хранилище
    header, signal = save_ecg_to_s3(params.id, header, signal)
    return header, signal
