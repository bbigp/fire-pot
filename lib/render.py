from datetime import datetime, timezone, timedelta
import hashlib
from typing import List, Callable, Any

from cachetools import TTLCache
from feedgen.feed import FeedGenerator
from nanoid import generate
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response
from lib.config import logger

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
    url: str=''
    maintainers: List[str]=[]
    handler: Callable[..., Any]
    example: str=''

    class Config:
        arbitrary_types_allowed=True

cache = TTLCache(maxsize=100, ttl=60*10)
def rss(request: Request, route: Route) -> Response:
    full_url = str(request.url)

    rss_feed_json = cache.get(full_url)
    if True:
    # if rss_feed_json is None:
        logger.info("Fetching RSS for %s", full_url)
        feed = route.handler(request)
        cache[full_url] = feed.json()
    else:
        feed = RSSFeed.parse_raw(rss_feed_json)

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

    for item in feed.item:
        fe = fg.add_entry()
        fe.id(item.id)
        fe.title(item.title)
        fe.link(href=item.link)
        fe.description(item.title)
        fe.pubDate(item.pubDate)
        fe.guid(item.link, permalink=True)
        fe.content(item.description)
    rss_feed = fg.rss_str(pretty=True)

    etag = hashlib.md5(rss_feed).hexdigest()
    headers = {
        "ETag": etag,
        "Last-Modified": now.strftime('%a, %d %b %Y %H:%M:%S +0000'),
    }
    return Response(content=rss_feed, media_type='application/xml', headers=headers)



