"""
Settings for the project.
"""

import os
from pathlib import Path

from argon2 import PasswordHasher
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# settings -env
load_dotenv(BASE_DIR / ".env")

# Settings DataBase
DATABASE = os.getenv("DATABASE")
DB_PATH = BASE_DIR / "data" / DATABASE

# Setting SuperUser
class ConfigAdmin:
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

# settings argon2
PH = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4, hash_len=32)
