import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# settings -env
load_dotenv(BASE_DIR / ".env")

DATABASE = os.getenv("DATABASE")
DB_PATH = BASE_DIR / "data" / DATABASE

# settings argon2