import os
import uuid
import aiofiles  # For asynchronous file operations
from fastapi import UploadFile
from dotenv import load_dotenv
from app.utils.validation import *
from app.utils.image_handler import *
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry




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
    
        imageHandler = UserImageHandler()
        file_path = await imageHandler.saveUserImage(user_id, image)
        


        # validate the uploaded image
        errors = validate_image(file_path, "")

        # Here you can insert metadata into a database, like user ID and file path
        # Example: db.insert({"user_id": user_id, "file_path": file_path})
        print(f"User {user_id} uploaded a file saved as {file_path}")


        return file_path, errors