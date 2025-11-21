import os
from dotenv import load_dotenv

load_dotenv()  # loads from .env automatically

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

settings = Settings()
