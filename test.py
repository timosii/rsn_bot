import requests
from bs4 import BeautifulSoup

from login import headers, index_payload_index, index_url, login_payload_user, login_user

session = requests.Session()
login_index = session.post(index_url, data=index_payload_index, headers=headers)
login_user = session.post(login_user, data=login_payload_user, headers=headers)

if login_index.status_code == 200 and login_user.status_code == 200:
    print('Авторизация прошла успешно')
else:
    print('Произошла ошибка авторизации')

# все посты -- собираем инфу
def all_posts(session: requests.Session=session) -> list:
    posts_metadata = []
    target_url_posts = "https://www.infinitestudio.art/scripts/fetch_posts.php"
    data_posts = {
        "limit": 24,
        "start": 0,
        "discussion": -1
    }

    response_posts = session.post(target_url_posts, data=data_posts, headers=headers)
    
    if response_posts.status_code == 200:
        posts = response_posts.json()["posts"]
        for post in posts:
            soup = BeautifulSoup(post["html"], 'lxml')
            profile_element = soup.find('img', class_='card-profile')
            profile_id = profile_element['onclick'].split("'")[1]
            title_element = soup.find('div', class_='card-title').get_text(strip=True, separator=' ')
            title = ' '.join(title_element.split()[:-1])
            refresh_time = title_element.split()[-1]
            posts_metadata.append({
                "id": post["id"],
                "user_id": profile_id,
                "title": title,
                "refresh_time": refresh_time
            })
            
        return posts_metadata
    
    else:
        print(f"Ошибка запроса списка всех постов: {response_posts.status_code}")
        raise Exception("Не удалось получить список всех постов")

def current_post(queue_post: int, posts_metadata: list, session: requests.Session=session) -> str:
    # текст поста -- передаются все посты и номер поста от 0 до 24, где 0 - самый свежий пост
    target_post_base_url = "https://www.infinitestudio.art/scripts/fetch_post.php"

    current_post = posts_metadata[queue_post]
    current_post_id = current_post["id"]

    data_current_post = {
        "post": current_post_id
    }

    response_target_post = session.post(target_post_base_url, data=data_current_post, headers=headers)

    if response_target_post.status_code == 200:
        content = response_target_post.json()["content"]
        soup = BeautifulSoup(content, 'lxml')
        content_text = '- ' + '\n- '.join(soup.stripped_strings)
        html = response_target_post.json()['html']
        soup_html = BeautifulSoup(html, 'lxml')
        user_name = soup_html.find('h5', class_='notranslate').text
        return f"Автор поста: {user_name}, текст:\n{content_text}"

    else:
        print(f"Ошибка запроса поста: {response_target_post.status_code}")
        raise Exception(f"Не удалось получить информацию о посте {current_post_id}")


def replies_post(post_id: str, session: requests.Session=session) -> str:
    # реплаи выбранного поста
    url_replies = "https://www.infinitestudio.art/scripts/fetch_replies.php"  
    data_replies = {
        "limit": 24,
        "start": 0,
        "post": post_id
    }
    
    response_replies = session.post(url_replies, data=data_replies, headers=headers)
    replies_fin = []
    if response_replies.status_code == 200:
        replies = response_replies.json()
        for reply in replies:
            content = reply["content"]
            soup = BeautifulSoup(content, 'lxml')
            content_text = '\n'.join(soup.stripped_strings)
            html_reply = reply['html']
            soup = BeautifulSoup(html_reply, 'lxml')
            user_name = soup.find('h5', id='post-title notranslate').text
            replies_fin.append({
                "author": user_name,
                "content": content_text
            })

    else:
        print(f"Ошибка запроса ветки поста: {response_replies.status_code}")
        raise Exception(f"Не удалось получить ответы поста {post_id}")

    replies_str = 'Ответы в посте:\n\n'
    for reply in replies_fin:
        replies_str += f"{reply['author']}:\n\n{reply['content']}\n\n"

    return replies_str


def take_post_id(posts_metadata: list, queue_post: int) -> str:
    return posts_metadata[queue_post]["id"] 
    


post_list = all_posts(session=session)
last_post = current_post(queue_post=0, posts_metadata=post_list, session=session)
post_id = take_post_id(queue_post=0, posts_metadata=post_list)
post_replies = replies_post(post_id=post_id)

print(last_post, post_replies)  

# формулирую, что должна делать программа
# 1. Отображать последний пост с возможностью открыть полностью с реплаями
# 2. Отображать последние 5 постов
# 3. Проверять - писали ли что-то в постах Руса (проверяем последние)
# 4. Проверять последние три поста
