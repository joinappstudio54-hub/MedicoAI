AI Food Image Analyzer (Gemini Vision + FastAPI)

This project is a FastAPI-based backend that uses Google Gemini Vision models to detect food items from images and return structured nutritional information in JSON format.

It has been tested across multiple food categories including fruits, beverages, snacks, and meals.

---

## :rocket: Features

- Detects whether an image contains food
- Identifies single or multiple food items
- Extracts structured nutrition data:
  - Product name
  - Category (fruit, beverage, snack, meal, dessert, dairy, vegetable, etc.)
  - Calories (estimated range)
  - Protein (estimated range)
  - Carbohydrates (estimated range)
  - Fat (estimated range)
  - Ingredients
- Handles both simple and complex food images
- Ensures strict JSON response format
- Prevents empty or partial outputs using validator

---

## :brain: AI Model

- Google Gemini Vision API
- Model used: `gemini-2.5-flash-lite`

> :warning: Note: Free-tier API has strict rate limits (approx. 20 requests/day)

---

## :package: API Endpoint

### `POST /api/upload`

Upload an image for food analysis.

---

## :inbox_tray: Request Format

- Method: `POST`
- Content-Type: `multipart/form-data`
- Field name: `image`

---

## :outbox_tray: Response Format

### :white_check_mark: Example (Single Food - Fruit)

```json
{
  "success": true,
  "message": ":white_check_mark: Food analyzed!",
  "data": {
    "is_food": true,
    "items": [
      {
        "product_name": "Mango",
        "category": "fruit",
        "calories": "150-200",
        "protein": "1-2g",
        "carbs": "35-45g",
        "fat": "0-1g",
        "ingredients": "mango"
      }
    ]
  }
}
```
