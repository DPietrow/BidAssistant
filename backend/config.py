import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SAM_MODE = os.getenv("SAM_MODE", "mock")

    SAM_API_KEY = os.getenv("SAM_API_KEY")
    
    SAM_API_URL = os.getenv(
        "SAM_API_URL",
        "https://api.sam.gov/opportunities/v2/search"
    )