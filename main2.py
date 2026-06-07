import requests
from bs4 import BeautifulSoup
import time
import re


KEYWORDS = ['дизайн', 'фото', 'web', 'python']

URL = 'https://habr.com/ru/all/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

DELAY_BETWEEN_REQUESTS = 1

def get_full_text(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('div', class_=re.compile(r'tm-article-body'))
        if content:
            return content.get_text().lower()
        return ''
    except Exception as e:
        print(f"Ошибка при загрузке статьи {url}: {e}")
        return ''

def get_articles_with_full_analysis():
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
        preview_text = (title + ' ' + (article.get_text() or '')).lower()
        if any(keyword.lower() in preview_text for keyword in KEYWORDS):
            print(f"{pub_date} – {title} – {link} (найдено в preview)")
            continue


        full_text = get_full_text(link)
        time.sleep(DELAY_BETWEEN_REQUESTS)

        if any(keyword.lower() in full_text for keyword in KEYWORDS):
            print(f"{pub_date} – {title} – {link} (найдено в полном тексте)")

if __name__ == '__main__':
    print("Расширенный анализ: проверяем preview и полный текст статей...")
    get_articles_with_full_analysis()
