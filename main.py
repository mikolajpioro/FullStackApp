from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
template = Jinja2Templates(directory='templates')