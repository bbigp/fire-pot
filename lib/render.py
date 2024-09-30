from datetime import datetime, timezone, timedelta
import hashlib
from typing import List, Callable, Any

from feedgen.feed import FeedGenerator
from nanoid import generate
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

from lib import cache
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


async def rss(request: Request, route: Route) -> Response:
    full_url = str(request.url)

    if True:
    # if not cache.exists_cahce(full_url):
        logger.info("Fetching RSS for %s", full_url)
        feed = await route.handler(request)
        cache.put_cahce(full_url, feed.json())
    else:
        feed = RSSFeed.parse_raw(cache.get_cahce(full_url))

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



