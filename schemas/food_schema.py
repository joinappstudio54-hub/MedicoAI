from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# ── Input from Gemini ──────────────────────────────────────────────────────────

class FoodItem(BaseModel):
    product_name: str = Field(default="")
    category:     str = Field(default="")
    calories:     str = Field(default="")
    protein:      str = Field(default="")
    carbs:        str = Field(default="")
    fat:          str = Field(default="")
    ingredients:  str = Field(default="")


class FoodData(BaseModel):
    is_food: bool
    items:   List[FoodItem] = Field(default_factory=list)


# ── API Responses ──────────────────────────────────────────────────────────────

class FoodResponse(BaseModel):
    success: bool
    message: str
    data:    FoodData


class CategoryOut(BaseModel):
    id:         int
    name:       str
    created_at: datetime

    class Config:
        from_attributes = True


class FoodItemOut(BaseModel):
    id:           int
    product_name: str
    category_id:  int
    category:     str = Field(validation_alias="category_name", default="")
    calories:     str
    protein:      str
    carbs:        str
    fat:          str
    ingredients:  str
    created_at:   datetime

    class Config:
        from_attributes = True


class FoodItemListResponse(BaseModel):
    success: bool
    count:   int
    data:    List[FoodItemOut]


class CategoryListResponse(BaseModel):
    success: bool
    count:   int
    data:    List[CategoryOut]


class SingleFoodResponse(BaseModel):
    success: bool
    data:    FoodItemOut
