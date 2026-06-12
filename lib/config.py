"""App configuration loaded from environment."""

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
APP_NAME = os.getenv("APP_NAME", "AuraWealth")
APP_TITLE = os.getenv("APP_TITLE", "AuraWealth - AI Wealth Management")
