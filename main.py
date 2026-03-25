from fastapi import FastAPI, Request
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
    }

]

@app.get("/", include_in_schema=False, name="home")
def home(request: Request):
    return template.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"})