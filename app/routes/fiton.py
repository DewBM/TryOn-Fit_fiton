import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.fiton_service import *
from pydantic import BaseModel;
from fastapi.responses import FileResponse


class FitonReqModel(BaseModel):
    user_id: str
    garment_url: str


router = APIRouter()


@router.post("/fiton")
async def virtual_fiton(reqBody: FitonReqModel):

    result = await FitOnService.fiton_garment(reqBody.user_id, reqBody.garment_url)
    print("Fiton Result: ", result)

    return result

@router.get("/fiton")
async def get_generated(image_path: str):
    path = Path(image_path)
    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Return the file as a response
    return FileResponse(image_path)
    # result = await FitOnService.getGeneratedImage(image_path)