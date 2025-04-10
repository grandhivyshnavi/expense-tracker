# config.py

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

DATABASE_URL = 'sqlite:///expenses.db'

# Email Config
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
