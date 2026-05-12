from fastapi import UploadFile, HTTPException
from PIL import Image
import io

def validate_image(file: UploadFile) -> bytes:
    """Validate image file type and size"""
    if not file.content_type.startswith('image/'):
        raise HTTPException(400, "❌ Only image files allowed!")
    
    content = file.file.read()
    try:
        Image.open(io.BytesIO(content)).verify()
        return content
    except:
        raise HTTPException(400, "❌ Invalid image!")