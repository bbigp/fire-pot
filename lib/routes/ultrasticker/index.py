import asyncio
from datetime import datetime, timezone, timedelta

from bs4 import BeautifulSoup
from starlette.requests import Request

from lib.cache import put_cache, exists_cache, get_cache
from lib.utils import logger
from lib.render import RSSFeed, Route, RSSItem
from lib.utils import ofetch
from main import app

host = 'https://cf.1761z.xyz/'
main_url = host + 'thread0806.php?fid=25'
LIMIT_RATE = 2


async def ctx(request: Request) -> RSSFeed:
    feed = gen_channel(url=main_url)

    new_items = []
    for each in feed.item:
        if exists_cache(each.link):
            each.description = get_cache(each.link)
            new_items.append(each)
        else:
            await details_queue.put(each.link)

    feed.item = new_items
    return feed


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
    d_data = ofetch.ofetch(link)
    item_soup = BeautifulSoup(d_data, 'html.parser')
    logger.info(f'GEN content {link}')
    description = item_soup.select_one('div#conttpc')
    return str(description).replace('ess-data=', 'src=')


route = Route(
    path='sdsd',
    name='',
    url='',
    maintainers = [],
    handler=ctx,
    content_handler=gen_content,
    example=''
)


