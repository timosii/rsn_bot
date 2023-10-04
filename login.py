from config import settings

password = settings.PASSWORD
access_key = settings.ACCESS_KEY
email = settings.EMAIL


headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
    }

# запрос логина и пароля
index_url = 'https://www.infinitestudio.art/users/index.php'
index_payload_index = {
    "tag": "login",
    "email": email,
    "password": password,
    "source": "web"
}

# запуск скрипта авторизации
login_user = "https://www.infinitestudio.art/scripts/login_user.php"
login_payload_user = {
    'user_id': '63c5b0134c2769.85149428',
    'access_key': access_key
}