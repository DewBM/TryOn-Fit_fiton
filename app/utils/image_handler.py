import os
import aiofiles  # For asynchronous file operations
from fastapi import UploadFile
from dotenv import load_dotenv
from pathlib import Path
import uuid
import shutil

class UserImageHandler:
    image_prefix = "user_"
    image_postfix = "_image"

    # Directory to store uploaded images
    UPLOAD_DIR = os.getenv("USER_IMAGE_DIR")
    
    def __init__(self) :
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)

    async def saveUserImage(self, user_id: str, image: UploadFile) -> str:
        # Generate a unique filename based on UUID
        file_extension = os.path.splitext(image.filename)[-1]
        unique_filename = f"{self.image_prefix}{user_id}{self.image_postfix}{file_extension}"

        # File path for saving
        file_path = os.path.join(self.UPLOAD_DIR, unique_filename)

        # Save the file asynchronously
        async with aiofiles.open(file_path, "wb") as f:
            content = await image.read()
            await f.write(content)

        return file_path


    async def getUserImageById(self, user_id: str) -> str:
        for file in os.listdir(self.UPLOAD_DIR):
            if os.path.splitext(file)[0] == f'{self.image_prefix}{user_id}{self.image_postfix}':
                file_path = os.path.join(self.UPLOAD_DIR, file)
                return file_path

        return ""



class GarmentImageHandler:
    UPLOAD_DIR = os.getenv('TEMP_IMAGE_DIR')

    def __init__(self) :
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)

    async def saveTempImage(self, image: UploadFile):
        # Generate a unique filename based on UUID
        file_extension = os.path.splitext(image.filename)[-1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        # File path for saving
        file_path = os.path.join(self.UPLOAD_DIR, unique_filename)

        # Save the file asynchronously
        async with aiofiles.open(file_path, "wb") as f:
            content = await image.read()
            await f.write(content)

        return file_path


class FitOnImageHandler:
    UPLOAD_DIR = os.getenv('GENERATED_IMAGE_DIR')

    def __init__(self) :
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)

    async def saveGeneratedImage(self, result):
        unique_filename = f"{uuid.uuid4()}.webp"

        # File path for saving
        output_file_path = os.path.join(self.UPLOAD_DIR, unique_filename)

        source_path = result[0]['image']

        # Copy the file to the new location
        try:
            shutil.copy(source_path, output_file_path)
            print(f"Output saved to: {output_file_path}")
            return output_file_path
        except FileNotFoundError:
            print(f"Source file not found: {source_path}")
        except Exception as e:
            print(f"Error while saving the file: {e}")
