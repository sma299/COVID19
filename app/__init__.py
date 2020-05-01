# shows the server where the application is

import os 
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV", default="development") # use "production" on a remote server