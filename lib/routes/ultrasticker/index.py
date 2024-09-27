from datetime import datetime, timezone

from bs4 import BeautifulSoup
from starlette.requests import Request

from lib.render import RSSFeed, Route, RSSItem
from lib.utils import ofetch

url = 'https://cf.1761z.xyz/thread0806.php?fid=25'
def ctx(request: Request) -> RSSFeed:
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
        link = 'https://cf.1761z.xyz/' + title_tag['href'].strip()
        id = title_tag['id']

        user = row.select_one('td a.bl').text.strip()
        post_time_tag = row.select_one('td div.f12 span.s3')
        post_time = post_time_tag['data-timestamp'].strip().replace('s', '')

        rss_item = RSSItem(id=id, title=title, link=link, author=user,
                           pubDate=datetime.fromtimestamp(int(post_time), tz=timezone.utc),
                           description='')
        rss_items.append(rss_item)

    return RSSFeed(title=r_title, link=url, description=r_description, item=rss_items)



route = Route(
    path='sdsd',
    name='',
    url='',
    maintainers = [],
    handler=ctx,
    example=''
)

data = ofetch.ofetch(url='https://cf.1761z.xyz/htm_data/2409/25/6519554.html')
print(data)