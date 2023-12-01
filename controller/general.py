import time

from model.all_post import Authors, take_post_list
from model.post_reply import current_post, replies_post
from view.display import post_and_replies, take_update_time_post, take_update_time_reply


def send_post(posts_count=1, time_wait=1, length_replies=5) -> str:
    '''
    Функция возвращает posts_count постов с реплаями. По дефолту -- последний пост
    '''
    post_list = take_post_list()
    res_post = ''

    for post in post_list[:posts_count]:
        post = current_post(post_id=post.id)
        replies = replies_post(post_id=post.id)
        res_post += post_and_replies(post=post, replies=replies, reply_count=length_replies)
        time.sleep(time_wait)
    return res_post


def send_sean_post(posts_count=1, time_wait=1, length_replies=5):
    '''
    Отправка постов Шона
    '''
    post_list = take_post_list()
    res = ''
    sean_posts = []
    count = 0
    for post in post_list:
        if post.author == Authors.Sean:
            sean_posts.append(post)
            post = current_post(post_id=post.id)
            replies = replies_post(post_id=post.id)
            res += post_and_replies(post=post, replies=replies, reply_count=length_replies)
            time.sleep(time_wait)
            count += 1
            if count == posts_count:
                break
    return res


def send_rsn_post(posts_count=1, time_wait=1, length_replies=5):
    '''
    Отправка последних постов пользователя Ruslan, либо тех, где он отвечал
    '''
    post_list = take_post_list()
    res = ''
    count = 0
    for post_info in post_list:
        post = current_post(post_id=post_info.id)
        replies = replies_post(post_id=post_info.id)
        if post_info.author == Authors.Ruslan:
            res += post_and_replies(post=post,
                                    replies=replies,
                                    reply_count=length_replies)
            time.sleep(time_wait)
            count += 1
        else:
            for reply in replies:
                if reply.user == "Ruslan":
                    res += post_and_replies(post=post,
                                            replies=replies,
                                            reply_count=length_replies)

                    count += 1
                    break

        if count == posts_count:
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
         
