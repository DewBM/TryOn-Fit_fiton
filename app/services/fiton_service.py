import os
import uuid
import aiofiles  # For asynchronous file operations
from fastapi import UploadFile
from dotenv import load_dotenv
from app.utils.image_handler import *
from pathlib import Path
from app.external.external_api import *
import shutil


class FitOnService:
    @staticmethod
    async def fiton_garment(user_id: str, garment_url: str) -> str:

        userImageHandler = UserImageHandler()
        # garmentImageHandler = GarmentImageHandler()
        fitonImageHandler = FitOnImageHandler()

        user_image = await userImageHandler.getUserImageById(user_id)
        # garment_image = await garmentImageHandler.saveTempImage(garment_image)

        if (user_image!=""):
            user_image_path = Path(user_image)
            result = await ExternalAPIClient.generateFitOn(user_image_path, garment_url)
            output_path = await fitonImageHandler.saveGeneratedImage(result)
            print('Output image: ', output_path)
            return {
                'isSuccess': True,
                'data': output_path,
                'msg': "Image updated successfully."
            }

        else:
            print("User image not found")
            return {
                'isSuccess': False,
                'data': None,
                'msg': "User image not found",
                'error': "User image not found"
            }