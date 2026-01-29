import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    """Base configuration."""
    PORT = int(os.environ.get("PORT", 5150))
    API_KEY = os.environ.get("API_KEY")
    if not API_KEY:
        raise ValueError("No API_KEY set for Flask application")
    DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
