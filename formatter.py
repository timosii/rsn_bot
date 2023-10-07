from logic.post_logic import Post
from logic.reply_logic import Reply

HELP_TEXT = "🔧 Отправляю посты с форума infinite_studio.art, ветка Beta Feedback. Умею:\n/last_post - отправлять последний пост\n/sean-отправлять последние 3 поста участника Sean Brakefield\n/ruslan - отправлять последние 3 поста, в которых писал Ruslan\n/when_update - отправлять дату последнего обновления ветки Beta Feedback.\n- Если ответов к посту больше 5 - отправляются последние 5\n- Иногда ответы очень длинные и не помещаются в пост телеграмма - тогда отправится последние 4, если не поместятся и они - то последние 3 ответа"

def form_post(post: Post) -> str:
    user = post.user
    content = post.content
    title = post.title
    return f"📩 <u><b>Post</b></u>:\n<i>{user}</i>\n\n<u>{title}</u>\n\n{content}\n\n✅ <b>Replies</b>:\n\n"
        

def form_replies(reply: Reply) -> str:
    user = reply.user
    content = reply.content
    res = f"👉<i>{user}</i>:\n{content}\n\n" if user else "<i>There is no replies ...</i>\n\n"
    return res

def take_update(reply: Reply) -> str:
    update = reply.update_time
    return f"⌛ The update was <b>{update}</b> ago"
