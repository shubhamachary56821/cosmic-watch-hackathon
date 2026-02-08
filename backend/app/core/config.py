import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    NASA_API_KEY: str = os.getenv("NASA_API_KEY") # type: ignore

settings = Settings()
