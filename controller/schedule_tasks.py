from controller.general import take_post_list
from model.all_post import Authors
from functools import wraps


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
        

def change_ids(rsn_post_id, sean_post_id):
    with open("ids.txt", 'w', encoding='utf-8') as file:
        file.write(f"rsn:{rsn_post_id} sean:{sean_post_id}")


def read_ids():
    with open("ids.txt", encoding='utf-8') as file:
        res = file.readlines()
    res = res[0].split()
    out = {}
    out["Rus"] = res[0].split(":")[-1]
    out["Sean"] = res[-1].split(":")[-1]
    return out


def length_control(func):
    def out(n):
        # n = args[0]
        while n > 0:
            try:
                res = func(n)
                return res
            except Exception:
                n -= 1
        return res
    return out


