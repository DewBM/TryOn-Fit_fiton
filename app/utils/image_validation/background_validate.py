# from segment_anything import SamAutomaticMaskGenerator
import cv2
import numpy as np
import mediapipe as mp
from ultralytics import YOLO

# def validate_background(image_path, segmentation_model):
#     import cv2
#     image = cv2.imread(image_path)
#     masks = segmentation_model.generate(image)
    
#     errors = []
#     if masks:
#         largest_mask = max(masks, key=lambda x: sum(sum(x['segmentation'])))
#         mask_area = sum(sum(largest_mask['segmentation']))
#         image_area = image.shape[0] * image.shape[1]
#         background_ratio = 1 - (mask_area / image_area)

#         if background_ratio > 0.5:
#             errors.append("Ensure the background is plain and uncluttered.")
#     return errors



def validate_background_uniformity(image_path, stddev_threshold=100):
    image = cv2.imread(image_path)
    blurred = cv2.GaussianBlur(image, (21, 21), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    stddev = np.std(gray)

    errors = []
    if stddev > stddev_threshold:
        errors.append("Background has too much variation. Use a simpler background.")

    return errors




def validate_background_edges(image_path, edge_threshold=1000):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(image, 50, 150)
    num_edges = np.sum(edges > 0)

    errors = []
    if num_edges > edge_threshold:
        errors.append("Background is too cluttered. Use a simpler background.")

    return errors



def validate_background_lighting(image_path, brightness_threshold=100):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    mean_brightness = np.mean(image)

    errors = []
    if mean_brightness < brightness_threshold:
        errors.append("Lighting is poor. Please ensure good lighting.")

    return errors




def validate_foreground_segmentation(image_path, foreground_threshold=0.3):
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    segmentor = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = segmentor.process(rgb_image)
    mask = results.segmentation_mask

    errors = []
    foreground_ratio = (mask > 0.5).mean()  # Ratio of foreground pixels
    if foreground_ratio < foreground_threshold:
        errors.append("Foreground is too small. Ensure the user fills the frame.")

    return errors




def validate_background_objects(image_path, max_objects=1):
    model = YOLO("yolov8n.pt")  # Use YOLO's smallest model
    results = model(image_path)

    errors = []
    num_objects = len(results[0].boxes)
    if num_objects > max_objects:
        errors.append(f"Background has {num_objects} objects. Use a simpler background.")

    return errors



def validate_background(image_path):
    errors = []

    # Validate uniformity
    errors.extend(validate_background_uniformity(image_path))

    # Validate edge clutter
    # errors.extend(validate_background_edges(image_path))

    # Validate lighting
    errors.extend(validate_background_lighting(image_path))

    # Validate foreground prominence
    # errors.extend(validate_foreground_segmentation(image_path))

    # Check for objects in the background
    errors.extend(validate_background_objects(image_path))

    return errors
