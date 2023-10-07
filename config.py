import os


class Settings:
    BOT_TOKEN = os.environ['BOT_TOKEN']
    MY_ID = os.environ['MY_ID']
    RSN_ID = os.environ['RSN_ID']
    PASSWORD = os.environ['PASSWORD']
    ACCESS_KEY = os.environ['ACCESS_KEY']
    EMAIL = os.environ['EMAIL']
    USER_ID = os.environ['USER_ID']
    TARGET_POST_URL = os.environ['TARGET_POST_URL']
    URL_REPLIES = os.environ['URL_REPLIES']
    INDEX_URL = os.environ['INDEX_URL']
    LOGIN_USER_URL = os.environ['LOGIN_USER_URL']

settings = Settings()