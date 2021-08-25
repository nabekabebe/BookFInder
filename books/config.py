import os
from dotenv import dotenv_values

config = dotenv_values(".env")

db_remote = config['DB_PATH_REMOTE']
db_local = config['DB_PATH_LOCAL']
GOOGLE_API_KEY = config['GOOGLE_API_KEY']
SECRET_KEY = config['SECRET_KEY']

SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"
DATABASE_URL = db_local if os.getenv('DATABASE_TYPE') == "LOCAL" else db_remote
