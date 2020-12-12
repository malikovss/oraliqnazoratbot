import os

from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("TOKEN")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB = os.getenv("DB")
DB_URL = f'postgres://{DB_PASS}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB}'
ADMIN = 1126854105
GID = -1001213911796
