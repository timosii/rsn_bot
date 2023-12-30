import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    MY_ID = os.getenv('MY_ID')
    RSN_ID = os.getenv('RSN_ID')
    PASSWORD = os.getenv('PASSWORD')
    ACCESS_KEY = os.getenv('ACCESS_KEY')
    EMAIL = os.getenv('EMAIL')
    USER_ID = os.getenv('USER_ID')
    TARGET_POST_URL = os.getenv('TARGET_POST_URL')
    URL_REPLIES = os.getenv('URL_REPLIES')
    INDEX_URL = os.getenv('INDEX_URL')
    LOGIN_USER_URL = os.getenv('LOGIN_USER_URL')

settings = Settings()