from general import take_post_list
from logic.base_logic import Authors


def check_last_sean_post():
    post_list = take_post_list()
    sean_posts = []
    for post in post_list[:5]:
        if post.author == Authors.Sean:
            sean_posts.append(post)

    if sean_posts:
        last_sean_post = sean_posts[0]
        return last_sean_post.id
 