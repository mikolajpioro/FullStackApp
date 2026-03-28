from fastapi import FastAPI, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
template = Jinja2Templates(directory='templates')


posts: list[dict] = [
    {
        "id": 1,
        "author": "John Lennon 123",
        "title": "Let's goooo",
        "content": "Hi. (I apologize for my bad English. I'm still learning and trying to improve my language skills. "
                "Sometimes, I might make mistakes or choose the wrong words,"
                " but I hope you can understand what I'm trying to say.)",
        "date_posted": "January 1, 2026"
    },
    {
        "id": 2,
        "author": "Jesus",
        "title": "Happy Birthday to me!",
        "content": "Merry Christmas",
        "date_posted": "December 25, 2025"
    },
    {
        "id": 3,
        "author": "John Wick",
        "title": "Pen",
        "content": "Where's my pen?",
        "date_posted": "December 25, 2000"
    },

]

@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False ,name="posts")
def home(request: Request):
    return template.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"})

@app.get("/posts/{post_id}", include_in_schema=False)
def post_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            title = post['title'][:50]
            return template.TemplateResponse(request, "post.html", {"post": post, "title": title})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Couldn't find this post")


@app.get("/api/posts")
def get_posts():
    return posts

@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Couldn't find this post")