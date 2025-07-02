import os

from dotenv import load_dotenv

load_dotenv()

# db
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "stats_tool")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

# Frontend
WEB_APP_URL = os.getenv('WEB_APP_URL', "http://localhost:5173")

