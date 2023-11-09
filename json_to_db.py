import json
from pathlib import Path

from models import Author, Quote
import connect

def load_data():


    # Завантаження даних авторів
    author_data_path = Path('json/authors.json')

    with open(author_data_path, 'r') as authors_file:
        authors_data = json.load(authors_file)

    for author_info in authors_data:
        author = Author(**author_info)
        author.save()


    # Завантаження даних цитат

    quote_info_path = Path('json/quotes.json')

    with open(quote_info_path, 'r') as quotes_file:
        quotes_data = json.load(quotes_file)

    for quote_info in quotes_data:
        author_name = quote_info["author"]
        author = Author.objects(fullname=author_name).first()
        if author:
            quote_info["author"] = author
            quote = Quote(**quote_info)
            quote.save()


if __name__ == '__main__':
    load_data()