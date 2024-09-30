import asyncio
import time
from datetime import datetime, timezone, timedelta

from bs4 import BeautifulSoup
from starlette.requests import Request

from lib.cache import get_cahce, exists_cahce, put_cahce
from lib.config import logger
from lib.render import RSSFeed, Route, RSSItem
from lib.utils import ofetch
from main import app

host = 'https://cf.1761z.xyz/'
main_url = host + 'thread0806.php?fid=25'
LIMIT_RATE = 2

details_queue = asyncio.Queue()
async def ctx(request: Request) -> RSSFeed:
    feed = gen_channel(url=main_url)

    new_items = []
    for each in feed.item:
        if exists_cahce(each.link):
            each.description = get_cahce(each.link)
            new_items.append(each)
        else:
            await details_queue.put(each.link)

    feed.item = new_items
    return feed

@app.on_event("startup")
def on_startup():
    asyncio.create_task(fetch_task())


async def fetch_task():
    while True:
        url = await details_queue.get()
        if url is None:
            await asyncio.sleep(2)
        else:
            await asyncio.sleep(LIMIT_RATE)  # 设置限速
            details = gen_content(url)
            put_cahce(url, details)

def gen_channel(url: str) -> RSSFeed:
    data = ofetch.ofetch(url=url)
    soup = BeautifulSoup(data, 'html.parser')
    r_title = soup.title.string + ' - Powered by RSSHub'
    r_description = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={
        'name': 'description'}) else 'No description found'

    tbody = soup.find('tbody', id="tbody")
    rows = tbody.select('tr.t_one')
    rss_items = []
    for row in rows:
        title_tag = row.select_one('td.tal h3 a')
        title = title_tag.text.strip()
        link = host + title_tag['href'].strip()
        id = title_tag['id']

        user = row.select_one('td a.bl').text.strip()
        post_time_tag = row.select_one('td div.f12 span.s3')
        post_time_title = post_time_tag['title']
        if '置顶主题' in post_time_title:
            naive_datetime = datetime.strptime(post_time_title.replace('置顶主题：', ''), "%Y-%m-%d %H:%M:%S")
            pubDate = naive_datetime.replace(tzinfo=timezone(timedelta(hours=8)))
        else:
            post_time = post_time_tag['data-timestamp'].strip().replace('s', '')
            pubDate = datetime.fromtimestamp(int(post_time), tz=timezone(timedelta(hours=8)))

        rss_item = RSSItem(id=id, title=title, link=link, author=user,
                           pubDate=pubDate,
                           description='')
        rss_items.append(rss_item)
    return RSSFeed(title=r_title, link=url, description=r_description, item=rss_items)


def gen_content(link: str) -> str:
    logger.info('client:%s', link)
    d_data = ofetch.ofetch(link)
    item_soup = BeautifulSoup(d_data, 'html.parser')
    logger.info('fetching item ' + link)
    description = item_soup.select_one('div#conttpc')
    return str(description).replace('ess-data=', 'src=')


route = Route(
    path='sdsd',
    name='',
    url='',
    maintainers = [],
    handler=ctx,
    example=''
)


