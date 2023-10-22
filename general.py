import time

from logic.base_logic import Authors, PostsList, all_posts, post_and_replies
from logic.login import login_process
from logic.post_logic import current_post
from logic.reply_logic import replies_post
from view import take_update_time_post, take_update_time_reply


def take_post_list() -> list[PostsList]:
    login_process()
    post_list = all_posts()
    return post_list


def send_post(seq_length=1, time_wait=1, length_replies=5) -> str:
    '''
    Функция возвращает seq_number постов с реплаями (с конца)
    '''
    post_list = take_post_list()
    res_post = ''

    for post in post_list[:seq_length]:
        res_post += post_and_replies(post.id, length=length_replies)
        time.sleep(time_wait)
        res_post += '---------------------------\n\n'
    print("Пост отправлен")
    return res_post


def send_sean_post(seq_length=3, time_wait=1, length_replies=5):
    '''
    Отправка постов Шона
    '''
    post_list = take_post_list()
    res = ''
    count = 0
    for post in post_list:
        if post.author == Authors.Sean:
            res += post_and_replies(post_id=post.id, length=length_replies)
            time.sleep(time_wait)
            res += '---------------------------\n\n'
            count += 1
            if count == seq_length:
                break

    return res


def send_rsn_post(seq_length=3, time_wait=1, length_replies=5):
    '''
    Отправка последних постов пользователя Ruslan
    '''
    post_list = take_post_list()
    res = ''
    count = 0
    for post in post_list:
        if post.author == Authors.Ruslan:
            res += post_and_replies(post_id=post.id, length=length_replies)
            res += '---------------------------\n\n'
            time.sleep(time_wait)
            count += 1
        else:
            replies = replies_post(post_id=post.id)
            for reply in replies:
                if reply.user == "Ruslan":
                    res += post_and_replies(post_id=post.id,
                                            length=length_replies)
                    res += '---------------------------\n\n'
                    count += 1
                    break

        if count == seq_length:
            break
    return res


def when_update():
    '''
    Функция возвращает время апдейта последнего поста
    '''
    post_list = take_post_list()
    last_post_id = post_list[0].id
    last_post = current_post(last_post_id)
    post_replies = replies_post(post_id=last_post_id)
    last_reply = post_replies[-1]
    res = take_update_time_reply(last_reply) if last_reply.update_time else take_update_time_post(last_post)
    return res


    

    

        
            
