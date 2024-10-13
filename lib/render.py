from datetime import datetime, timezone, timedelta
import hashlib
from typing import List, Callable, Any, Dict

from feedgen.feed import FeedGenerator
from nanoid import generate
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

from lib import cache
from lib.cron import details_queue
from lib.utils import logger


class RSSItem(BaseModel):
    id: str=''
    title: str=''
    author: str=''
    pubDate: datetime=None
    link: str=''
    description: str=''

class RSSFeed(BaseModel):
    title: str=''
    link: str=''
    description: str=''
    item: List[RSSItem]=[]

class Route(BaseModel):
    path: str=''
    name: str=''
    example: str=''
    parameters: Dict=[]
    handler: Callable[..., Any]
    content_handler: Callable[..., Any]
    description: str=''

    class Config:
        arbitrary_types_allowed=True

class BackgroundTask(BaseModel):
    route: Route
    link: str

    def execute(self):
        data = self.route.content_handler(self.link)
        cache.put_cache(self.link, data, ttl=60*60*24*5)

    class Config:
        arbitrary_types_allowed = True

async def rss(request: Request, route: Route) -> Response:
    full_url = str(request.url)
    cache_key = 'RSS-Channel:' + full_url

    data = cache.get_cache(cache_key)
    if data is None:
        logger.info(f"[Render] data from network --> {full_url}")
        feed = await route.handler(request)
        cache.put_cache(cache_key, feed.json(), ttl=60 * 5)
    else:
        logger.info(f'[Render] data from cache --> {full_url}')
        feed = RSSFeed.parse_raw(data)

    return_items = []
    for each in feed.item:
        if cache.exists_cache(each.link):
            each.description = cache.get_cache(each.link)
            return_items.append(each)
        else:
            await details_queue.put(BackgroundTask(route=route, link=each.link))


    now = datetime.now(timezone(timedelta(hours=8)))
    fg = FeedGenerator()
    fg.id(generate(size=10))
    fg.title(feed.title)
    fg.link(href=feed.link, rel='alternate')
    fg.description(feed.description)
    fg.generator('bigp-rsshub')
    fg.webMaster('https://register-ui.onlybox.cn/')
    fg.language('zh')
    fg.lastBuildDate(now)

    for item in return_items:
        fe = fg.add_entry()
        fe.id(item.id)
        fe.title(item.title)
        fe.link(href=item.link)
        fe.description(item.title)
        fe.pubDate(item.pubDate)
        fe.guid(item.link, permalink=True)
        fe.content(f"<![CDATA[{item.description}]]>")
    rss_feed = fg.rss_str(pretty=True)

    etag = hashlib.md5(rss_feed).hexdigest()
    headers = {
        "ETag": etag,
        "Last-Modified": now.strftime('%a, %d %b %Y %H:%M:%S +0000'),
    }
    return Response(content=rss_feed, media_type='application/xml', headers=headers)



