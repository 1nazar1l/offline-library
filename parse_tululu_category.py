from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from main import download_txt, download_image, parse_book_page,check_for_redirect
import json
import os


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


for page in range(1, 5):
    books_page_url = f'https://tululu.org/l55/{page}'
    response = requests.get(books_page_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all(class_="d_book")
    for book in books:
        try:
            book_id = book.find("a")["href"]
            book_id = book_id.split("/")[1]
            url = 'https://tululu.org'
            book_url = urljoin(url,book_id)
            response = requests.get(book_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            book = parse_book_page(soup)
            print('Название: ', book['title'])
            print('Автор:', book['author'])
            download_dict(book)

            img_url = book['img_url']
            img_url = urljoin(url, img_url)
            book_id = book_id[1:]
            filename = f'{book_id}'
            download_image(filename, img_url)

            title = book['title']
            params = {'id': {book_id}}
            url = 'https://tululu.org/txt.php'
            response = requests.get(url, params=params)
            response.raise_for_status() 
            check_for_redirect(response)
            filename = f'{book_id}. {title}'
            download_txt(response, filename)

        except requests.HTTPError:
            print('Not found book')