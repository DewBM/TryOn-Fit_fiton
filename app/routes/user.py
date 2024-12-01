import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.user_service import UserService

router = APIRouter()


@router.post("/user-image")
async def upload_user_image(
        user_id: str = Form(...),  # User ID from the request
        image: UploadFile = File(...),  # Uploaded image file
):
    # Validate the file type (optional, e.g., only JPEG and PNG are allowed)
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are allowed.")

    # Delegate to the service to handle the file and metadata
    saved_filename, errors = await UserService.process_and_save_user_image(user_id, image)

    if (len(errors)==0):
        return {
            "isSuccess": True,
            "msg" : "Image uploaded successfully"
        }

    else:
        if os.path.exists(saved_filename):
            os.remove(saved_filename)
        return {
            "isSuccess": False,
            "msg" : "Image validation failed. Try uploading another image.",
            "errord": errors
        }