import os
from pathlib import Path
from dotenv import load_dotenv

# ✅ Correct path for backend folder
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    def __init__(self):
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self._validate()

    def _validate(self):
        if not self.GEMINI_API_KEY:
            raise ValueError("❌ GEMINI_API_KEY missing in .env")

settings = Settings()