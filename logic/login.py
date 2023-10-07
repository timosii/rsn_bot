import requests
from fake_headers import Headers

from config import settings

password = settings.PASSWORD
access_key = settings.ACCESS_KEY
email = settings.EMAIL
user_id = settings.USER_ID
index_url = settings.INDEX_URL
login_user_url = settings.LOGIN_USER_URL


header = Headers(
    browser='firefox',
    os='lin'
)
headers = header.generate()

# data запроса логина и пароля
index_payload_index = {
    "tag": "login",
    "email": email,
    "password": password,
    "source": "web"
}

# data запроса на авторизацию
login_payload_user = {
    'user_id': user_id,
    'access_key': access_key
}

session = requests.Session()

def login_process():
    login_index = session.post(index_url,
                           data=index_payload_index,
                           headers=headers)
    login_script = session.post(login_user_url, data=login_payload_user, headers=headers)
    
    if login_index.status_code == 200 and login_script.status_code == 200:
        print('Авторизация прошла успешно')
    else:
        print('Произошла ошибка авторизации')
        raise Exception("Ошибка авторизации")

