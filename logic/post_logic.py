from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

from config import settings

from .login import headers, session

target_post_url = settings.TARGET_POST_URL

@dataclass
class Post:
    id: str
    user: str
    title: str
    content: str
    

def current_post(post_id: str,                 
                 session: requests.Session = session) -> Post:
    post_id = post_id
    data_current_post = {"post": post_id}
    response_target_post = session.post(target_post_url,
                                        data=data_current_post,
                                        headers=headers)

    if response_target_post.status_code == 200:
        title = response_target_post.json()["subject"]
        content = response_target_post.json()["content"]
        soup = BeautifulSoup(content, 'lxml')
        content_text = '\n'.join(soup.stripped_strings)
        html = response_target_post.json()['html']
        soup_html = BeautifulSoup(html, 'lxml')
        user_name_element = soup_html.find('h5', class_='notranslate')
        user_name = user_name_element.text if user_name_element else "Неизвестный юзер"
        result = Post(id=post_id, user=user_name, title=title, content=content_text)
        return result

    else:
        print(f"Ошибка запроса поста: {response_target_post.status_code}")
        raise Exception(
            f"Не удалось получить информацию о посте {post_id}")