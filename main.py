import requests
from bs4 import BeautifulSoup
import re


KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com/ru/all/'


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

def get_articles_preview():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article', class_=re.compile(r'tm-articles-list__item'))

    for article in articles:
        time_tag = article.find('time')
        pub_date = time_tag['datetime'].split('T')[0] if time_tag else 'Неизвестно'

        h2 = article.find('h2')
        if not h2:
            continue
        a = h2.find('a')
        if not a:
            continue
        title = a.text.strip()
        link = 'https://habr.com' + a['href']

        preview_div = article.find('div', class_=re.compile(r'tm-article-snippet'))
        preview_text = preview_div.text.lower() if preview_div else ''

        search_text = (title + ' ' + preview_text).lower()

        if any(keyword.lower() in search_text for keyword in KEYWORDS):
            print(f"{pub_date} – {title} – {link}")

if __name__ == '__main__':
    print("Поиск статей...")
    get_articles_preview()
