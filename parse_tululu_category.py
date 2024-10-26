from bs4 import BeautifulSoup
import requests

from urllib.parse import urljoin
from parse_tululu_books import download_txt, download_image, parse_book_page,check_for_redirect, get_all_books
import argparse
import sys
import time
import os


def main():
    parser = argparse.ArgumentParser(description="Скачивает книги определенного жанра и информацию о них")
    parser.add_argument('--start_page', type=int, default="1", help='Введите с какой страницы начать скачивать книги:')
    parser.add_argument('--end_page', type=int, help='Введите какой страницей закончить скачивание книг:')
    parser.add_argument('--dest_folder', type=str,default="library",help='Укажите папку в которую будет сохраняться вся информация')
    parser.add_argument('--skip_imgs', help="Укажите это значение чтобы пропустить скачивание картинок", action='store_true')
    parser.add_argument('--skip_txt', help="Укажите это значение чтобы пропустить скачивание текста", action='store_true')
    args = parser.parse_args()

    root_folder = args.dest_folder
    all_books = []

    if args.start_page == 1 and not args.end_page:
        end_page = 5
    elif not args.end_page:
        end_page = args.start_page + 1
        print("Конечное значение не указано поэтому будет скачана 1 страница")
    elif args.start_page > args.end_page:
        print("Начальное значение не может быть больше конечного.")
        sys.exit(1)
    else:
        end_page = args.end_page

    for page in range(args.start_page, end_page):
        try:
            books_page_url = f'https://tululu.org/l55/{page}'
            response = requests.get(books_page_url)
            response.raise_for_status()
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'html.parser')
            selector = ".d_book"
            books = soup.select(selector)
            for book in books:
                book_id = book.a["href"]
                book_id = book_id.split("/")[1]
                url = 'https://tululu.org'
                book_url = os.path.join(f'{url}{book_id}/')

                response = requests.get(book_url)
                response.raise_for_status()
                check_for_redirect(response)

                soup = BeautifulSoup(response.text, 'html.parser')
                book = parse_book_page(soup)
                all_books.append(book)

                print('Название: ', book['title'])
                print('Автор:', book['author'])

                if not args.skip_imgs:
                    img_url = book['img_url']
                    img_url = urljoin(url, img_url)
                    book_id = book_id[1:]
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

        except requests.HTTPError:
            print('Not found book')

        except requests.ConnectionError:
            time.sleep(5)
            print("Not connection, please wait")

    get_all_books(all_books, root_folder)

if __name__ == "__main__":
    main()