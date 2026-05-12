from fastapi import APIRouter, UploadFile, File, HTTPException
from services.gemini_service import analyze_food
from utils.image_utils import validate_image
from schemas.food_schema import FoodResponse

router = APIRouter()

@router.post("/upload", response_model=FoodResponse)
async def upload_image(file: UploadFile = File(...)):
    # 1. Validate image
    image_bytes = validate_image(file)
    
    # 2. Analyze with Gemini
    result = await analyze_food(image_bytes)
    
    # 3. Check if food detected
    if not result["is_food"]:
        raise HTTPException(400, "🍔 No food detected! Please upload food image.")
    
    # 4. Format beautiful response (<100 tokens)
    return FoodResponse(
        success=True,
        message="✅ Food analyzed!",
        data=result
    )