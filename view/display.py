from model.post_reply import Post, Reply


def html_fix(text: str) -> str:
    return text.replace('&', '&amp;').replace('>', '&gt;').replace('<', '&lt;')


def form_post(post: Post) -> str:
    user = html_fix(post.user)
    content = html_fix(post.content)
    title = html_fix(post.title)
    return f"📩 <u><b>Post</b></u>:\n<i>{user}</i>\n\n<u>{title}</u>\n\n{content}\n\n✅ <b>Replies</b>:\n\n"
        

def form_reply(reply: Reply) -> str:
    user = html_fix(reply.user)
    content = html_fix(reply.content)
    res = f"👉<i>{user}</i>:\n{content}\n\n" if user else "<i>There is no replies ...</i>\n\n"
    return res


def post_and_replies(post: Post, replies: list[Reply]=None, reply_count=5) -> str:
    res = form_post(post=post)
    if replies:
        if len(replies) > reply_count:
            replies = replies[-reply_count:]
        for reply in replies:
            res += form_reply(reply=reply)
    return res


def take_update_time_reply(reply: Reply) -> str:
    update = reply.update_time
    return f"⌛ The update was <b>{update}</b> ago"

def take_update_time_post(post: Post) -> str:
    update = post.update_time
    return f"⌛ The update was <b>{update}</b> ago"
