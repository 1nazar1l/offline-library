import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

import os
from urllib.parse import urljoin
import argparse
import time
import json

def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(response, filename, root_folder, folder="books/"):
    os.makedirs(f'{root_folder}/{folder}', exist_ok=True)

    filepath = os.path.join(f'{sanitize_filename(root_folder)}/{folder}{sanitize_filename(filename)}.txt')
    with open(filepath, 'w', encoding='UTF-8') as f:
        f.write(response.text)


def download_image(filename, img_url, root_folder, folder="images/"):
    os.makedirs(f'{root_folder}/{folder}', exist_ok=True)

    if 'nopic' in img_url:
        filename = 'nopic'

    response = requests.get(img_url)
    response.raise_for_status()
    
    file_extension = os.path.splitext(img_url)[1]
    filepath = os.path.join(f'{sanitize_filename(root_folder)}/{folder}{filename}{file_extension}')

    with open(filepath, 'wb') as f:
        f.write(response.content)


def append_books_dict(books, root_folder):
    os.makedirs(sanitize_filename(root_folder), exist_ok=True)

    filename = "books_dict.json"
    filepath = os.path.join(f'{sanitize_filename(root_folder)}/{filename}')

    with open(filepath, 'w', encoding='UTF8') as f:
        json.dump(books, f, ensure_ascii=False, indent=4)


def parse_book_page(soup):
    title_tag = soup.h1.text.split(" :: ")
    title, author = title_tag

    selector = "span.d_book a"
    genres = [genre.text for genre in soup.select(selector)]


    selector = ".texts span"
    comments = [comment.text for comment in soup.select(selector)]

    selector = ".bookimage img"
    img_url = soup.select_one(selector)["src"]

    book = {
        'title': title.strip(),
        'author': author.strip(),
        'genres': genres,
        'comments': comments,
        'img_url': img_url
    }

    return book


def main():
    parser = argparse.ArgumentParser(description="Скачивает книги и информацию о них")
    parser.add_argument('--start_id', type=int, default="1", help='Введите с какого id начать скачивать книги:')
    parser.add_argument('--end_id', type=int, default="10", help='Введите каким id закончить скачивание книг:')
    parser.add_argument('--dest_folder', type=str,default="library",help='Укажите папку в которую будет сохраняться вся информация')
    parser.add_argument('--skip_imgs', help="Укажите это значение чтобы пропустить скачивание картинок", action='store_true')
    parser.add_argument('--skip_txt', help="Укажите это значение чтобы пропустить скачивание текста", action='store_true')
    args = parser.parse_args()
    books = []
    root_folder = args.dest_folder

    for book_id in range(args.start_id, args.end_id):
        try:

            url = f'https://tululu.org/b{book_id}/'
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'html.parser')
            book = parse_book_page(soup)
            print('Название: ', book['title'])
            print('Автор:', book['author'])
            books.append(book)

            if not args.skip_imgs:
                img_url = book['img_url']
                img_url = urljoin(url, img_url)
                filename = f'{book_id}'
                download_image(filename, img_url, root_folder)

            if not args.skip_txt:
                title = book['title']
                params = {'id': {book_id}}
                url = 'https://tululu.org/txt.php'
                response = requests.get(url, params=params)
                response.raise_for_status() 
                check_for_redirect(response)
                filename = f'{book_id}. {title}'
                download_txt(response, filename, root_folder)

            book_id += 1

        except requests.HTTPError:
            print('Not found book')

        except requests.ConnectionError:
            time.sleep(5)
            print("Not connection, please wait")

    append_books_dict(books, root_folder)

if __name__ == '__main__':
    main()
