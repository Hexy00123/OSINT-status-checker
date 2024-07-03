from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter(prefix="/qr", tags=["Qr"])

URL_IMAGE_QR = "qr_image.png"

@router.get("/")
async def create():
    image_path = Path(URL_IMAGE_QR)
    if not image_path.is_file():
        return {"error": "QR image not found in server"}
    return FileResponse(image_path)
