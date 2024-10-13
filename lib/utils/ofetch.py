import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from lib.utils import logger

DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
urllib3.disable_warnings(InsecureRequestWarning)

def ofetch(url: str, headers=None, proxies: dict=None) -> str:
    logger.info(f"[Requesting] ---> {url}")
    if headers is None:
        headers = DEFAULT_HEADERS
    try:
        res = requests.get(url, headers=headers, proxies=proxies, verify=False)
        res.raise_for_status()
        return res.text
    except Exception as e:
        logger.error(f'[Err] {e}')
        raise e


# async def fetch_by_puppeteer(url):
#     try:
#         from pyppeteer import launch
#     except Exception as e:
#         print(f'[Err] {e}')
#     else:
#         browser = await launch(  # 启动浏览器
#             {'args': ['--no-sandbox']},
#             handleSIGINT=False,
#             handleSIGTERM=False,
#             handleSIGHUP=False
#         )
#         page = await browser.newPage()  # 创建新页面
#         await page.goto(url)  # 访问网址
#         html = await page.content()  # 获取页面内容
#         await browser.close()  # 关闭浏览器
#         return Selector(text=html)