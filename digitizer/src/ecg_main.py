from pathlib import Path

import cv2
import numpy as np

from scaling_enter import convertECGLeads
from ecgdigitize.image import openImage
from model.InputParameters import InputParameters
from model.Lead import Lead, LeadId

def show_img(img):
    window_name = 'photo'
    cv2.imshow(window_name, img)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
    cv2.waitKey(0)
    cv2.destroyWindow(window_name)


def main():
    DATASET_PATH = '/home/semyon/ecg/digitizing/images-dataset-600'
    ROI_PATH = f"{DATASET_PATH}/00001_lr-0-I.png"

    roi = cv2.imread(ROI_PATH)
    ROI_X, ROI_Y, ROI_H, ROI_W, _ = 0, 0, *roi.shape
    leads = {LeadId.I: Lead(x=ROI_X, y=ROI_Y, width=ROI_W, height=ROI_H, startTime=0)}

    path = Path(ROI_PATH)
    image = openImage(path)
    params = InputParameters(
        rotation=0,
        timeScale=25,
        voltScale=10,
        leads=leads
    )
    extracted_signals, preview_images = convertECGLeads(image, params)

    lead_img = preview_images[LeadId.I].data
    lead_signal = extracted_signals[LeadId.I]
    lead_signal = lead_signal[~np.isnan(lead_signal)]

    print(lead_signal)
    print(np.sum(np.isnan(lead_signal)))
    print(len(lead_signal))

    show_img(lead_img)


if __name__ == "__main__":
    main()
