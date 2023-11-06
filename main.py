import requests
from bs4 import BeautifulSoup
import json
from models import Author, Quote
import connect

# Отримання цитат та авторів зі сторінки
def scrape_quotes_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    quotes = []

    for quote_div in soup.find_all('div', class_='quote'):
        quote_text = quote_div.find('span', class_='text').get_text()
        author_name = quote_div.find('small', class_='author').get_text()
        author = Author.objects(fullname=author_name).first()

        if not author:
            author = Author(fullname=author_name)
            author.save()

        tags = [tag.get_text() for tag in quote_div.find_all('a', class_='tag')]
        quote = Quote(quote=quote_text, author=author, tags=tags)
        quote.save()

        quotes.append(quote)

    return quotes

# Отримання посилань на наступні сторінки
def get_next_page_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    next_page_link = soup.find('li', class_='next').find('a')
    if next_page_link:
        next_page_url = next_page_link['href']
        if not next_page_url.startswith('http'):
            next_page_url = f"http://quotes.toscrape.com{next_page_url}"
        return next_page_url
    else:
        return None



# Основна функція для скрапінгу всіх сторінок сайту
def scrape_all_pages(url):
    all_quotes = []
    while url:
        if not url.startswith('http'):
            url = f"http://quotes.toscrape.com{url}"
        quotes = scrape_quotes_page(url)
        all_quotes.extend(quotes)
        url = get_next_page_url(url)

    return all_quotes


if __name__ == '__main__':
    base_url = 'http://quotes.toscrape.com'
    all_quotes = scrape_all_pages(base_url)

    with open('quotes.json', 'w') as quotes_file:
        json.dump(all_quotes, quotes_file, indent=2)

    # Збереження авторів
    authors_data = [{'fullname': author.fullname, 'born_date': author.born_date, 'born_location': author.born_location,
                     'description': author.description} for author in Author.objects]

    with open('authors.json', 'w') as authors_file:
        json.dump(authors_data, authors_file, indent=2)