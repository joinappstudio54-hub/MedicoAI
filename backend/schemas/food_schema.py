# from pydantic import BaseModel
# from typing import Optional

# class FoodData(BaseModel):
#     is_food: bool
#     product_name: Optional[str] = ""
#     category: Optional[str] = ""
#     calories: Optional[str] = ""
#     protein: Optional[str] = ""
#     carbs: Optional[str] = ""
#     fat: Optional[str] = ""
#     ingredients: Optional[str] = ""

# class FoodResponse(BaseModel):
#     success: bool
#     message: str
#     data: Optional[FoodData] = None



# new


from pydantic import BaseModel, Field
from typing import List, Optional

class FoodItem(BaseModel):
    product_name: str = Field(default="")
    category: str = Field(default="")
    calories: str = Field(default="")
    protein: str = Field(default="")
    carbs: str = Field(default="")
    fat: str = Field(default="")
    ingredients: str = Field(default="")

class FoodData(BaseModel):
    is_food: bool
    items: List[FoodItem] = Field(default_factory=list)

class FoodResponse(BaseModel):
    success: bool
    message: str
    data: FoodData