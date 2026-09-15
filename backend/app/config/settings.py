import os
from dotenv import load_dotenv

load_dotenv() # read .env and load all into os.environ

class Settings:
    def __init__(self):
        self.deno_path = os.environ["DENO_PATH"]
        self.pot_server_url = os.environ["POT_SERVER_URL"]