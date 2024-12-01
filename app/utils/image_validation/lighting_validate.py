import cv2
import numpy as np
from skimage import exposure

def validate_lighting(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    brightness = np.mean(image)
    contrast = exposure.is_low_contrast(image, fraction_threshold=0.35)

    errors = []
    if brightness < 50 or brightness > 250:
        errors.append("Ensure good, even lighting in the image.")
    if contrast:
        errors.append("Image contrast is too low.")
    return errors
