# from fastapi import APIRouter
# from app.schemas.meal_schema import MealRequest
# from app.services.validation_service import validate_all
# from fastapi import APIRouter, HTTPException

# router = APIRouter()



# @router.post("/step-2-body")
# def step_2_body(data: MealRequest):
#     result = validate_all(data.dict())

#     if "errors" in result:
#         return {
#             "status": "error",
#             "errors": result["errors"]
#         }

#     return {
#         "status": "success",
#         "data": result
#     }



import json
from click import prompt
from fastapi import APIRouter, HTTPException
from app.schemas.meal_schema import MealRequest
from app.services.validation_service import validate_all
from app.services.prompt_service import build_prompt
from app.services.gemini_service import generate_meal
from app.utils.json_parser import safe_parse_json


router = APIRouter()


@router.post("/step-2-body")
def step_2_body(data: MealRequest):
    result = validate_all(data.dict())

    if "errors" in result:
        raise HTTPException(
            status_code=422,
            detail=result["errors"]
        )

    return {
        "status": "success",
        "data": result
    }



# @router.post("/generate-meal-plan")
# def generate_meal_plan(data: MealRequest):
#     result = validate_all(data.model_dump())

#     # ❌ validation error
#     if "errors" in result:
#         raise HTTPException(status_code=422, detail=result["errors"])

#     # ✅ build prompt from CLEAN data
#     # prompt = build_prompt(result)
#     prompt = build_prompt(data.model_dump())

    
#     try:
#         # 🤖 generate from Gemini
#         output = generate_meal(prompt)
        
#         clean_output = output.strip()
#         # Clean markdown if present
#         if clean_output.startswith("```json"):
#             clean_output = clean_output[7:]
#         elif clean_output.startswith("```"):
#             clean_output = clean_output[3:]
#         if clean_output.endswith("```"):
#             clean_output = clean_output[:-3]
            
#         # Parse the JSON
#         parsed_meals = json.loads(clean_output.strip())
        
#         # Verify basic structure
#         if not isinstance(parsed_meals, dict) or "meals" not in parsed_meals:
#             raise HTTPException(status_code=500, detail="Invalid meal plan structure generated.")
            
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         # If it fails to parse or Gemini fails, return the error detail
#         raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

#     return {
#         "status": "success",
#         "meal_plan": parsed_meals
#     }

# try check 

@router.post("/generate-meal-plan")
def generate_meal_plan(data: MealRequest):
    result = validate_all(data.model_dump())

    if "errors" in result:
        raise HTTPException(status_code=422, detail=result["errors"])

    prompt = build_prompt(data.model_dump())

    try:
        parsed_meals = None

        for _ in range(2):
            output = generate_meal(prompt)

            clean_output = output.strip()

            if clean_output.startswith("```json"):
                clean_output = clean_output[7:]
            elif clean_output.startswith("```"):
                clean_output = clean_output[3:]
            if clean_output.endswith("```"):
                clean_output = clean_output[:-3]

            # parsed_meals = json.loads(clean_output.strip())
 
           
            parsed_meals = safe_parse_json(clean_output)

            if not isinstance(parsed_meals, dict) or "meals" not in parsed_meals:
                continue

            summary = parsed_meals.get("nutrition_breakdown", {})
            total_cal = summary.get("total_calories", 0)
            total_protein = summary.get("total_protein_g", 0)

            target_cal = parsed_meals["summary"]["target_calories"]
            target_protein = parsed_meals["summary"]["target_protein_g"]

            if abs(total_cal - target_cal) <= 50 and abs(total_protein - target_protein) <= 5:
                break

        if parsed_meals is None:
            raise HTTPException(status_code=500, detail="Failed to generate valid meal plan")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
   

   
    return {
        "status": "success",
        "meal_plan": parsed_meals
    }