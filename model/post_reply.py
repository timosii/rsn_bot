from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

from config import settings

from .connection import headers, session

target_post_url = settings.TARGET_POST_URL
url_replies = settings.URL_REPLIES


@dataclass
class Post:
    id: str
    user: str
    title: str
    content: str
    update_time: str
    

@dataclass
class Reply:
    user: str
    content: str
    update_time: str


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
        update_time_element = soup_html.find('p', class_="card-subtext notranslate") 
        update_time = update_time_element.text if update_time_element else "Время обновления неизвестно"        
        result = Post(id=post_id, user=user_name, title=title, content=content_text, update_time=update_time)
        return result

    else:
        print(f"Ошибка запроса поста: {response_target_post.status_code}")
        raise Exception(
            f"Не удалось получить информацию о посте {post_id}")
       

def replies_post(post_id: str, session: requests.Session = session) -> list[Reply]:
    data_replies = {"limit": 96, "start": 0, "post": post_id}

    response_replies = session.post(url_replies,
                                    data=data_replies,
                                    headers=headers)
    replies_fin = []
    if response_replies.status_code == 200:
        if response_replies.text:
            replies = response_replies.json()
            for reply in replies:
                content = reply["content"]
                soup = BeautifulSoup(content, 'lxml')
                content_text = '\n'.join(soup.stripped_strings)
                html_reply = reply['html']
                soup = BeautifulSoup(html_reply, 'lxml')
                user_name_element = soup.find('h5', id='post-title notranslate')
                user_name = user_name_element.text if user_name_element else "Неизвестный"
                update_time_element = soup.find('p', class_="card-subtext notranslate") 
                update_time = update_time_element.text if update_time_element else "Время обновления неизвестно"
                replies_fin.append(Reply(user=user_name, content=content_text, update_time=update_time))
        else:
            replies_fin.append(Reply(user='', content='', update_time=''))
        
    
    else:
        print(f"Ошибка запроса ветки поста: {response_replies.status_code}")
        raise Exception(f"Не удалось получить ответы поста {post_id}")

    return replies_fin    

