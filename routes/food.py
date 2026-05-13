from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from services.gemini_service import analyze_food
from services.db_service import (
    save_food_items,
    get_all_categories,
    get_all_food_items,
    get_food_by_id,
    get_food_by_category_id,
    search_food,
)
from utils.image_utils import validate_image
from schemas.food_schema import *

router = APIRouter()


@router.post('/upload', response_model=FoodResponse, status_code=status.HTTP_201_CREATED)
async def upload_image(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    image_bytes, image_hash = await validate_image(file)

    result = await analyze_food(image_bytes)

    if result.get('error'):
        raise HTTPException(status_code=503, detail=result['error'])

    if not result.get('is_food'):
        raise HTTPException(
            status_code=400,
            detail='No food item detected. Please upload again.',
        )

    saved_items = await save_food_items(db, result['items'], image_hash)
    await db.commit()

    return FoodResponse(
        success=True,
        message=f'{len(saved_items)} food item(s) analyzed successfully.',
        data=FoodData(**result),
    )


@router.get('/categories', response_model=CategoryListResponse)
async def get_categories(db: AsyncSession = Depends(get_db)):
    categories = await get_all_categories(db)
    return {
        'success': True,
        'count': len(categories),
        'data': categories,
    }


@router.get('/foods', response_model=FoodItemListResponse)
async def get_foods(db: AsyncSession = Depends(get_db)):
    items = await get_all_food_items(db)
    return {
        'success': True,
        'count': len(items),
        'data': items,
    }


@router.get('/foods/search', response_model=FoodItemListResponse)
async def search_food_items(
    q: str = Query(..., min_length=2, max_length=100),
    db: AsyncSession = Depends(get_db),
):
    items = await search_food(db, q)
    return {
        'success': True,
        'count': len(items),
        'data': items,
    }


@router.get('/foods/{food_id}', response_model=SingleFoodResponse)
async def get_single_food(food_id: int, db: AsyncSession = Depends(get_db)):
    item = await get_food_by_id(db, food_id)

    if not item:
        raise HTTPException(status_code=404, detail='Food item not found.')

    return {'success': True, 'data': item}


@router.get('/foods/category/{category_id}', response_model=FoodItemListResponse)
async def get_foods_by_category(category_id: int, db: AsyncSession = Depends(get_db)):
    items = await get_food_by_category_id(db, category_id)

    return {
        'success': True,
        'count': len(items),
        'data': items,
    }
