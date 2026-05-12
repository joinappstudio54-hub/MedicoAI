import json
import re
from typing import Dict, Any
from schemas.food_schema import FoodData

def parse_gemini_json(raw_text: str) -> Dict[str, Any]:
    """Extract and validate JSON from Gemini response"""
    try:
        # Clean JSON from markdown
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
        else:
            json_str = raw_text.strip()
        
        data = json.loads(json_str)
        return FoodData(**data).dict()
    except:
        return {"is_food": False}
