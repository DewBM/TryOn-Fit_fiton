from app.utils.image_validation.pose_validate import validate_pose
from app.utils.image_validation.lighting_validate import validate_lighting
from app.utils.image_validation.background_validate import validate_background
from app.utils.image_validation.clothing_validate import validate_clothing

def validate_image(image_path, segmentation_model):
    errors = []
    errors.extend(validate_pose(image_path))
    errors.extend(validate_lighting(image_path))
    # errors.extend(validate_background(image_path, segmentation_model))
    errors.extend(validate_background(image_path))
    errors.extend(validate_clothing(image_path))
    return errors
