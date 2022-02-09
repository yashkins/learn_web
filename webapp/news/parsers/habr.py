from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import locale
import platform
from webapp.news.parsers.utils import get_html, save_news

if platform.system() == "Windows":
    locale.setlocale(locale.LC_ALL, "russian")
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU')

def parser_time(str_time):
    if "сегодня" in str_time:
        today = datetime.now()
        str_time = str_time.replace("сегодня", today.strftime("%d %B %Y"))
    elif "вчера" in str_time:
        yesterday = datetime.now() - timedelta(days=1)
        str_time = str_time.replace("вчера", yesterday.strftime("%d %B %Y"))
    else:
        str_time = str_time[:16]
        try:
            return datetime.strptime(str_time, '%Y-%m-%dT%H:%M')
        except ValueError:
            return datetime.now()
    try:
        return datetime.strptime(str_time, '%d %B %Y в %H:%M')
    except ValueError:
        return datetime.now()

def get_habr_snippets():
    html = get_html('https://habr.com/ru/search/?target_type=posts&q=python&order')
    if html:
        soup = BeautifulSoup(html,'html.parser')
        all_news = soup.find('div', class_='tm-articles-list').findAll('div', class_='tm-article-snippet') 
        for news in all_news:
            title = news.find('a', class_='tm-article-snippet__title-link').text
            url = 'https://habr.com' + news.find('a', class_='tm-article-snippet__title-link')['href']
            published = news.find('time')['datetime']
            published = parser_time(published)
            save_news(title, url, published)
            