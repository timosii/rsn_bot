from controller.general import take_post_list
from model.all_post import Authors
from model.database import change_len, change_sean, take_data
from model.post_reply import replies_post


def last_sean_post_id():
    post_list = take_post_list()
    for post in post_list:
        if post.author == Authors.Sean:
            return post.id


def check_new_sean_post() -> int:
    '''Функция возвращает максимальный пост -- то есть самый свежий
    '''
    post_list = take_post_list()
    sean_id_list = [int(post.id) for post in post_list if post.author == Authors.Sean]
    return max(sean_id_list)
    
    
def last_rsn_post_id():
    post_list = take_post_list()
    for post in post_list:
        if post.author == Authors.Ruslan:
            return post.id


def control_rus_replies():
    post_list = take_post_list()
    rsn_post = None
    for post in post_list:
        if post.author == Authors.Ruslan:
            rsn_post = post.id
            break
    if rsn_post:
        replies_rsn = replies_post(rsn_post)
        replies_without_rsn = [reply for reply in replies_rsn if reply.user != Authors.Ruslan]
        len_replies = len(replies_without_rsn)
        return len_replies
        

def change_ids(sean_post_id, len_rus_replies):
    change_sean(sean_post_id)
    change_len(len_rus_replies)


def read_ids():
    out = {}
    sean, len_rus = take_data()
    out["Sean"] = sean
    out["Len"] = len_rus
    return out
