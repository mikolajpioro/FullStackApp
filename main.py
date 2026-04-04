from fastapi import FastAPI, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from schemas import PostCreate, PostResponse


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
def home_page(request: Request):
    return template.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"})

@app.get("/posts/{post_id}", include_in_schema=False)
def post_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            title = post['title'][:50]
            return template.TemplateResponse(request, "post.html", {"post": post, "title": title})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Couldn't find this post")




# api pages -----------------------------------------------
@app.get("/api/posts", response_model=list[PostResponse])
def get_posts():
    return posts

@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Couldn't find this post")

@app.post("/api/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED,)
def create_post(post: PostCreate):
    new_id = 0
    if posts:
        ids = []
        for p in posts:
            ids.append(p["id"])
        new_id = max(ids) + 1
    else:
        new_id = 1
    new_post = {
        "id": new_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "date_posted": "December 25, 2026",
    }
    posts.append(new_post)
    return new_post
# --------------------------------------------------------

# Error handling -----------------------------------------
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error has occured, Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return template.TemplateResponse(request,"error.html", {"status_code": exception.status_code, "title": exception.status_code, "message": message}, status_code=exception.status_code,)



@app.exception_handler(RequestValidationError)
def validation_exception(request: Request, execption: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": execption.errors()},
        )
    
    return template.TemplateResponse(request, "error.html", {"status_code": status.HTTP_422_UNPROCESSABLE_CONTENT, "title": status.HTTP_422_UNPROCESSABLE_CONTENT, "message": "Invalid request. Please check your input and try again."}, status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,)
# ---------------------------------------------------------