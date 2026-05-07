import os
from dotenv import load_dotenv

load_dotenv()

KIMI_API_KEY = os.getenv("KIMI_API_KEY")
KIMI_API_URL = os.getenv("KIMI_API_URL")

GITLAB_URL = os.getenv("GITLAB_URL")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
