from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

from logic.post_logic import current_post
from logic.reply_logic import replies_post
from view import form_post, form_reply

from .login import headers, session


@dataclass
class PostsList:
    id: str
    author: str
    title: str
    create_time: str

@dataclass
class Authors:
    Sean: str = '06342536'
    Ruslan: str = '85149428'

# все посты -- собираем инфу
def all_posts(session: requests.Session = session) -> list[PostsList]:
    posts_metadata = []
    target_url_posts = "https://www.infinitestudio.art/scripts/fetch_posts.php"
    data_posts = {
        "limit": 24, 
        "start": 0, 
        "discussion": -1
    }

    response_posts = session.post(target_url_posts,
                                  data=data_posts,
                                  headers=headers)

    if response_posts.status_code == 200:
        posts = response_posts.json()["posts"]
        for post in posts:
            soup = BeautifulSoup(post["html"], 'lxml')
            img_tag = soup.find('img', class_='card-profile')
            img_path = img_tag["src"] if img_tag else "Тег src не найден"
            author_id = img_path.split('/')[-2]
            title_element_raw = soup.find('div', class_='card-title')
            if title_element_raw:
                title_element = title_element_raw.get_text(
                strip=True, separator=' ')
                title = ' '.join(title_element.split()[:-1])
                create_time = title_element.split()[-1]
            else:
                title = "Неизвестный заголовок"
                create_time = "Время обновления неизвестно"

            posts_metadata.append(
                PostsList(id=post["id"], author=author_id, title=title, create_time=create_time)
            )
        return posts_metadata
    else:
        print(
            f"Ошибка запроса списка всех постов: {response_posts.status_code}")
        raise Exception("Не удалось получить список всех постов")


def post_and_replies(post_id: str, length=5):
    '''
    Получает post_id, возвращает пост и его реплаи - уже строкой
    '''
    post = current_post(post_id=post_id)
    replies = replies_post(post_id=post_id)
    res = form_post(post)
    if len(replies) > length:
        replies = replies[-length:]
    for reply in replies:
        res += form_reply(reply)
    return res
    
    
        