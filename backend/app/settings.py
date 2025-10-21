from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
DATABASE_KEY = os.getenv('DATABASE_KEY')

JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')

class Settings:
    database_url: str = DATABASE_URL
    database_key: str = DATABASE_KEY

    jwt_algorithm: str = JWT_ALGORITHM
    jwt_secret: str = JWT_SECRET

settings = Settings()