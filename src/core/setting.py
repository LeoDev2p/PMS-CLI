import os
from pathlib import Path

from argon2 import PasswordHasher
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# settings -env
load_dotenv(BASE_DIR / ".env")

DATABASE = os.getenv("DATABASE")
DB_PATH = BASE_DIR / "data" / DATABASE

# settings argon2
PH = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4, hash_len=32)
