import hashlib
from datetime import datetime

from fastapi import APIRouter
from feedgen.feed import FeedGenerator
from starlette.requests import Request
from starlette.responses import Response
from starlette.templating import Jinja2Templates

from lib import render

request_mapping = APIRouter()
templates = Jinja2Templates(directory='lib/templates')

@request_mapping.get("/")
async def index(request: Request):
    return templates.TemplateResponse('index.html', context={
        'request': request
    })



@request_mapping.get("/ultrasticker/")
async def ultrasticker(request: Request):
    from lib.routes.ultrasticker.index import route
    return render.rss(request, route)
