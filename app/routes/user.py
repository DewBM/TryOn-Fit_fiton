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

    return {"message": "Image uploaded successfully!", "filename": saved_filename, "errors: ": errors}