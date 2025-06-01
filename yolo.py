
import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np

image = cv2.imread("IMAGE DIRECTORY")
model = YOLO("yolo11_100epoch.pt")

def callback(image_slice: np.ndarray) -> sv.Detections:
    result = model(image_slice)[0]
    return sv.Detections.from_ultralytics(result)


slicer = sv.InferenceSlicer(callback = callback)

sliced_detections = slicer(image)
label_annotator = sv.LabelAnnotator()
box_annotator = sv.BoxAnnotator()

annotated_image = box_annotator.annotate(
    scene=image.copy(), detections=sliced_detections)

annotated_image = label_annotator.annotate(
    scene=annotated_image, detections=sliced_detections)

sv.plot_image(annotated_image)

#REF LINK: https://blog.roboflow.com/how-to-use-sahi-to-detect-small-objects/