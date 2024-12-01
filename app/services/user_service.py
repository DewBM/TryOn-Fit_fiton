import os
import uuid
import aiofiles  # For asynchronous file operations
from fastapi import UploadFile
from dotenv import load_dotenv
from app.utils.validation import *
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry

# Directory to store uploaded images
UPLOAD_DIR = os.getenv("USER_IMAGE_DIR")
os.makedirs(UPLOAD_DIR, exist_ok=True)


class UserService:
    @staticmethod
    async def process_and_save_user_image(user_id: str, image: UploadFile) -> str:
        """
        Handles the processing and saving of the uploaded user image.
        - Saves the file to the filesystem with a unique name.
        - Performs any additional logic like storing metadata in a database.

        :param user_id: The ID of the user uploading the image.
        :param image: The uploaded file object.
        :return: The name of the saved file.
        """
        # Generate a unique filename based on UUID
        file_extension = os.path.splitext(image.filename)[-1]
        unique_filename = f"user_{user_id}_image{file_extension}"

        # File path for saving
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # Save the file asynchronously
        async with aiofiles.open(file_path, "wb") as f:
            content = await image.read()
            await f.write(content)


        # validate the uploaded image
        errors = validate_image(file_path, "")

        # Here you can insert metadata into a database, like user ID and file path
        # Example: db.insert({"user_id": user_id, "file_path": file_path})
        print(f"User {user_id} uploaded a file saved as {unique_filename}")


        return file_path, errors
