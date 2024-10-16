from datetime import datetime

from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from lib import render

request_mapping = APIRouter()
templates = Jinja2Templates(directory='lib/templates')

@request_mapping.get("/")
async def index(request: Request):
    from lib.routes.b_1761z.index import route
    return templates.TemplateResponse('index.html', context={
        'request': request,
        'routes': [route, route, route, route]
    })

next_execute_time = 0
@request_mapping.get('/schedule_task')
async def schedule_task(request:Request):
    global next_execute_time
    now = int(datetime.now().timestamp())
    next_execute_time = now if next_execute_time == 0 else next_execute_time
    if now >= next_execute_time:
        do_task()
        return 'success'
    return 'skip'

def do_task():
    global next_execute_time
    next_execute_time = int(datetime.now().timestamp()) + 5

@request_mapping.get("/1761z/{fid}")
async def ultrasticker(request: Request):
    from lib.routes.b_1761z.index import route
    return await render.rss(request, route)
