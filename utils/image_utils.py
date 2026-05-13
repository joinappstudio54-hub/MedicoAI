from fastapi import UploadFile, HTTPException
from PIL import Image
import io
import hashlib

MIN_SIZE_KB = 10  # Minimum 10 KB to prevent tiny icons/blank files
MAX_SIZE_MB = 5   # Maximum 5 MB to prevent massive uploads

async def validate_image(file: UploadFile) -> tuple[bytes, str]:
    """Validate image file type and size"""
    if not file.content_type.startswith('image/'):
        raise HTTPException(400, "❌ Only image files allowed!")
    
    content = await file.read()
    
    # File size validation
    size_kb = len(content) / 1024
    if size_kb < MIN_SIZE_KB:
        raise HTTPException(400, f"❌ Image is too small ({size_kb:.1f} KB). Please upload an image of at least {MIN_SIZE_KB} KB.")
        
    size_mb = size_kb / 1024
    if size_mb > MAX_SIZE_MB:
        raise HTTPException(400, f"❌ Image is too large ({size_mb:.1f} MB). Maximum size is {MAX_SIZE_MB} MB.")

    try:
        Image.open(io.BytesIO(content)).verify()
        image_hash = hashlib.md5(content).hexdigest()
    
        return content, image_hash
    except Exception:
        raise HTTPException(400, "❌ Invalid image!")