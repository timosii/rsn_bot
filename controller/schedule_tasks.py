from controller.general import take_post_list
from model.all_post import Authors
from model.post_reply import replies_post


def last_sean_post_id():
    post_list = take_post_list()
    for post in post_list:
        if post.author == Authors.Sean:
            return post.id
        
    
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
        return str(len_replies)
        

def change_ids(sean_post_id, len_rus_replies):
    with open("ids.txt", 'w', encoding='utf-8') as file:
        file.write(f"sean:{sean_post_id} len:{len_rus_replies}")


def read_ids():
    with open("ids.txt", encoding='utf-8') as file:
        res = file.readlines()
    res = res[0].split()
    out = {}
    out["Sean"] = res[0].split(":")[-1]
    out["Len"] = res[1].split(":")[-1]
    return out


def length_replies_control(func):
    def out(*args, **kwargs):
        n = kwargs['length_replies']
        while n > 0:
            try:
                res = func(*args, **kwargs)
                return res
            except Exception:
                n -= 1
        return res
    return out


