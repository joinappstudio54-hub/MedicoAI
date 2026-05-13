# Food AI API

A FastAPI service that analyzes uploaded food images using Google Gemini and stores detected food items in a PostgreSQL database.

## Features

- Upload an image for food recognition
- Analyze multiple visible food items in a single image
- Store detected food items with category, nutrition estimates, and ingredients
- Query stored food items, categories, details, and search results
- Auto-creates the database schema on startup

## Requirements

- Python 3.11+
- PostgreSQL database with an async connection URL
- Google Gemini API key

## Setup

1. Create a Python virtual environment:

```bash
python -m venv .venv
```

2. Activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Create a `.env` file in the project root with:

```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql+asyncpg://user:password@host:port/dbname
APP_NAME=Food AI API
DEBUG=True
```

## Running the API

Start the app using Uvicorn on localhost:

```bash
uvicorn main:app --reload
```

Then open:

- `http://127.0.0.1:8000/` for a health check
- `http://127.0.0.1:8000/docs` for interactive API documentation

To make the API available to other devices on your local network, bind to all interfaces:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Then access it from another PC using your host machine IP, for example:

- `http://192.168.10.19:8000/api/categories`
- `http://192.168.10.19:8000/api/foods/category/1`

## API Endpoints

### `POST /api/upload`

- Upload a food image file
- Returns recognized food items, category, nutrition estimates, and ingredients
- Request body: `multipart/form-data` with field `file`

### `GET /api/categories`

- Returns stored categories

### `GET /api/foods`

- Returns all stored food items

### `GET /api/foods/search?q=<query>`

- Search food items by product name or ingredients

### `GET /api/foods/{food_id}`

- Returns details for a specific food item

### `GET /api/foods/category/{category_id}`

- Returns food items in a specific category

## Database

- Uses SQLAlchemy Async ORM
- Database models are defined in `db/models.py`
- The schema is created automatically on app startup via the FastAPI lifespan hook

## Project Structure

- `main.py` — FastAPI application setup
- `config.py` — settings loaded from `.env`
- `db/` — async database engine, session, and models
- `routes/food.py` — API route definitions
- `schemas/food_schema.py` — request/response Pydantic models
- `services/` — Gemini analysis and database persistence logic
- `utils/validator.py` — Gemini JSON parsing and validation

## Notes

- The app uses Google Gemini to analyze image content and expects valid JSON in the response.
- If Gemini returns malformed output, the app defaults to `is_food: false`.
- Duplicate detection is supported via `image_hash` saved in food item records.
