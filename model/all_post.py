from dataclasses import dataclass
from model.connection import headers, login_process, session


import requests
from bs4 import BeautifulSoup


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
def take_post_list(session: requests.Session = session) -> list[PostsList]:
    posts_metadata = []
    login_process()
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
    

    
    
        