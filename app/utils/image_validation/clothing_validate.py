import cv2
import numpy as np

def validate_clothing(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(edges) / edges.size

    errors = []
    if edge_density > 1.0:
        errors.append("Avoid wearing patterned or textured clothing.")
    return errors
