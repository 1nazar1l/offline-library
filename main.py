import requests
import os
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
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


def download_txt(url, filename, folder="books/"):
    os.makedirs("books", exist_ok=True)

    response = requests.get(url)
    response.raise_for_status() 
    check_for_redirect(response)

    filepath = os.path.join(f'{folder}{sanitize_filename(filename)}.txt')
    with open(filepath, 'w', encoding='UTF-8') as f:
        f.write(response.text)


def download_image(filename, soup, folder="images/"):
    os.makedirs("images", exist_ok=True)

    img_url = soup.find(class_='bookimage').find('img')['src']
    if 'nopic' in img_url:
        filename = 'nopic'

    img_url = urljoin('https://tululu.org/', img_url)
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

    genres_block = soup.find('span', class_ = 'd_book').find_all('a')
    correct_genres = []
    for genre in genres_block:
        genre_text = genre.text
        correct_genres.append(genre_text)

    comments_block = soup.find_all(class_ = 'texts')
    correct_comments = []
    if comments_block:
        for comment in comments_block:
            comment = comment.find('span')
            comment_text = comment.text
            correct_comments.append(comment_text)

    book = {
        'title': title,
        'author': author,
        'genres': correct_genres,
        'comments': correct_comments
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

            filename = f'{book_id}'
            download_image(filename, soup)

            title = get_title(soup)
            url = f'https://tululu.org/txt.php?id={book_id}'
            filename = f'{book_id}. {title}'
            download_txt(url, filename)

            book_id += 1

        except requests.HTTPError:
            print('Not found book')

        except requests.ConnectionError:
            time.sleep(50)
            print("Not connection, please wait")


if __name__ == '__main__':
    main()
