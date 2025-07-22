import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    MONGODB_URI = os.getenv("MONGODB_URI")
    WEBSITE_BASE_URL = os.getenv("WEBSITE_BASE_URL", "https://yourdomain.com")
