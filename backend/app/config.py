import os
from dotenv import load_dotenv

load_dotenv()

SPORTMONKS_API_KEY = os.getenv("SPORTMONKS_API_KEY")
FOOTBALL_DATA_API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
ODDS_API_KEY = os.getenv("ODDS_API_KEY")

BASE_URL = "https://api.sportmonks.com/v3/football"