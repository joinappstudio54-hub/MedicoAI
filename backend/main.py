from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.food import router

app = FastAPI(title="🍔 Food AI API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def home():
    return {"message": "🍔 Food AI Backend Ready!", "upload": "/api/upload"}