import requests
from bs4 import BeautifulSoup

import os
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
import argparse
import time


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_title(soup):
    text = soup.find('h1').text
    main_info = text.split(" :: ")
    title = main_info[0].replace(u'\xa0', u' ').strip()
    return title


def download_txt(url, filename, params, folder="books/"):
    os.makedirs("books", exist_ok=True)

    response = requests.get(url, params=params)
    response.raise_for_status() 
    check_for_redirect(response)

    filepath = os.path.join(f'{folder}{sanitize_filename(filename)}.txt')
    with open(filepath, 'w', encoding='UTF-8') as f:
        f.write(response.text)


def download_image(filename, img_url, folder="images/"):
    os.makedirs("images", exist_ok=True)

    if 'nopic' in img_url:
        filename = 'nopic'

    response = requests.get(img_url)
    response.raise_for_status()
    
    file_extension = os.path.splitext(img_url)[1]
    filepath = os.path.join(f'{folder}{filename}{file_extension}')

    with open(filepath, 'wb') as f:
        f.write(response.content)


def parse_book_page(soup):
    title_tag = soup.find('h1').text
    main_info = title_tag.split(" :: ")
    title = main_info[0].replace(u'\xa0', u' ').strip()
    author = main_info[1].replace(u'\xa0', u' ').strip()

    genres = soup.find('span', class_ = 'd_book').find_all('a')
    genres = [genre.text for genre in genres]

    comments = soup.find_all(class_ = 'texts')
    if comments:
        comments = [comment.find('span').text for comment in comments]

    img_url = soup.find(class_='bookimage').find('img')['src']


    book = {
        'title': title,
        'author': author,
        'genres': genres,
        'comments': comments,
        'img_url': img_url
    }

    return book


def main():
    parser = argparse.ArgumentParser(description="Скачивает книги и информацию о них")
    parser.add_argument('--start_id', type=int, default="1", help='Введите с какого id начать скачивать книги:')
    parser.add_argument('--end_id', type=int, default="10", help='Введите каким id закончить скачивание книг:')
    args = parser.parse_args()

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

            img_url = book['img_url']
            img_url = urljoin(url, img_url)
            filename = f'{book_id}'
            download_image(filename, img_url)

            title = get_title(soup)
            params = {'id': {book_id}}
            url = 'https://tululu.org/txt.php'
            filename = f'{book_id}. {title}'
            download_txt(url, filename, params)

            book_id += 1

        except requests.HTTPError:
            print('Not found book')

        except requests.ConnectionError:
            time.sleep(50)
            print("Not connection, please wait")


if __name__ == '__main__':
    main()
