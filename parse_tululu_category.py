from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from main import download_txt, download_image, parse_book_page,check_for_redirect
import json
import os
import argparse
import sys

def download_dict(book):
    if os.path.exists('books_dict.json'):
            # Загружаем существующие данные
            with open('books_dict.json', 'r', encoding='UTF8') as f:
                books = json.load(f)
    else:
        # Если файл не существует, создаем новый список
        books = []

    # Добавляем новый элемент в список
    books.append(book)

    # Сохраняем обновленный список обратно в файл
    with open('books_dict.json', 'w', encoding='UTF8') as f:
        json.dump(books, f, ensure_ascii=False, indent=4)


parser = argparse.ArgumentParser(description="Скачивает книги и информацию о них")
parser.add_argument('--start_page', type=int, default="1", help='Введите с какой страницы начать скачивать книги:')
parser.add_argument('--end_page', type=int, help='Введите какой страницей закончить скачивание книг:')
args = parser.parse_args()
if args.start_page == 1 and args.end_page is None:
    end_page = 5
elif args.end_page is None:
    end_page = args.start_page + 1
    print("Конечное значение не указано поэтому будет скачана 1 страница")
elif args.start_page > args.end_page:
    print("Начальное значение не может быть больше конечного.")
    sys.exit(1)
else:
    end_page = args.end_page

for page in range(args.start_page, end_page):
    books_page_url = f'https://tululu.org/l55/{page}'
    response = requests.get(books_page_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    selector = ".d_book"
    books = soup.select(selector)
    for book in books:
        try:
            book_id = book.a["href"]
            book_id = book_id.split("/")[1]
            url = 'https://tululu.org'
            book_url = urljoin(url,book_id)
            print(book_url)
            response = requests.get(book_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            book = parse_book_page(soup)
            print('Название: ', book['title'])
            print('Автор:', book['author'])
            download_dict(book)
            print("add_dict - OK")

            img_url = book['img_url']
            img_url = urljoin(url, img_url)
            book_id = book_id[1:]
            filename = f'{book_id}'
            download_image(filename, img_url)
            print("Download img - OK")

            title = book['title']
            params = {'id': {book_id}}
            url = 'https://tululu.org/txt.php'
            response = requests.get(url, params=params)
            response.raise_for_status() 
            check_for_redirect(response)
            filename = f'{book_id}. {title}'
            download_txt(response, filename)
            print("Download text - OK")

        except requests.HTTPError:
            print('Not found book')