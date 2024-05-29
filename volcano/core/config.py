# NOTE This file is for const variables such as DB URL
# LINK please refer this: https://github.com/jujumilk3/fastapi-clean-architecture/blob/main/app/core/config.py
from dotenv import load_dotenv


load_dotenv()

import os

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
APP_NAME = "VolcanoAPI"
VERSION = "v1.0.0"

# it must be a new line for cd
