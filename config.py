import os


class Settings:
    BOT_TOKEN = os.environ['BOT_TOKEN']
    MY_ID = os.environ['MY_ID']
    RSN_ID = os.environ['RSN_ID']
    PASSWORD = os.environ['PASSWORD']
    ACCESS_KEY = os.environ['ACCESS_KEY']
    EMAIL = os.environ['EMAIL']

settings = Settings()