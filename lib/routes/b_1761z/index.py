from datetime import datetime, timezone, timedelta

from bs4 import BeautifulSoup
from starlette.requests import Request

from lib.render import RSSFeed, Route, RSSItem
from lib.utils import logger
from lib.utils import ofetch

host = 'https://cf.1761z.xyz/'
main_url = host + 'thread0806.php?fid='


async def ctx(request: Request) -> RSSFeed:
    fid = request.path_params['fid']
    feed = gen_channel(url=main_url + fid)
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


def ctx_for_description(link: str) -> str:
    d_data = ofetch.ofetch(link)
    item_soup = BeautifulSoup(d_data, 'html.parser')
    logger.info(f'GEN detail {link}')
    description = item_soup.select_one('div#conttpc')
    return str(description).replace('ess-data=', 'src=')


route = Route(
    path='/1761z/:fid',
    name='分区帖子',
    example='/1761z/25',
    parameters={'fid': '分区id'},
    handler=ctx,
    content_handler=ctx_for_description,
    description='国产原创区：25'
)


