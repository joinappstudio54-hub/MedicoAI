# from google import genai
# from config import settings
# from utils.validator import parse_gemini_json

# # ✅ create client
# client = genai.Client(api_key=settings.GEMINI_API_KEY)

# async def analyze_food(image_bytes: bytes) -> dict:
#     prompt = """Analyze food image. RETURN ONLY VALID JSON:

# NO FOOD: {"is_food":false}

# FOOD:
# {"is_food":true,"product_name":"","category":"","calories":"","protein":"","carbs":"","fat":"","ingredients":""}"""

#     response = client.models.generate_content(
#         model="gemini-2.5-flash-lite",
#         contents=[
#             prompt,
#             {
#                 "inline_data": {
#                     "mime_type": "image/jpeg",
#                     "data": image_bytes
#                 }
#             }
#         ]
#     )

#     return parse_gemini_json(response.text)


from google import genai
from config import settings
from utils.validator import parse_gemini_json

# ✅ create client
client = genai.Client(api_key=settings.GEMINI_API_KEY)

async def analyze_food(image_bytes: bytes) -> dict:

    prompt = """Analyze food image. RETURN ONLY VALID JSON:

    NO FOOD: {"is_food": false}

    FOOD - List ALL visible items:
    {
    "is_food": true,
    "items": [
        {
        "product_name": "EXACT food/drink name",
        "category": "food type (pizza, beverage, dessert, etc)",
        "calories": "estimated calories (e.g. 250-350)",
        "protein": "estimated protein (e.g. 10-15g)",
        "carbs": "estimated carbs (e.g. 30-40g)",
        "fat": "estimated fat (e.g. 8-12g)",
        "ingredients": "main ingredients you see"
        }
    ]
    }
    RULES:
    - Multiple foods = multiple items in array
    - Always estimate nutrition values
    - Be specific with names """

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[
            prompt,
            {
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": image_bytes
                }
            }
        ]
    )

    return parse_gemini_json(response.text)
