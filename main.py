import requests
import os
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError

def get_title(id):
    url = f'https://tululu.org/b{id}/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.find('h1').text
    book = text.split(" :: ")
    title = book[0].replace(u'\xa0', u' ').strip()
    return title

def download_txt(url, filename, folder="books/"):
    os.makedirs("books", exist_ok=True)
    response = requests.get(url)
    response.raise_for_status() 
    check_for_redirect(response)
    filepath = os.path.join(f'{folder}{sanitize_filename(filename)}.txt')
    with open(filepath, 'w', encoding='UTF-8') as f:
        f.write(response.text)


def download_image(url, filename, folder="images/"):
    os.makedirs("images", exist_ok=True)

    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'html.parser')
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


def get_comments(url):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    comments = soup.find_all(class_ = 'texts')
    if comments:
        for comment in comments:
            comment = comment.find('span')
            comment_text = comment.text
            print(comment_text)
    else:
        print("No comments")

def get_genre(url):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    genres = soup.find('span', class_ = 'd_book').find_all('a')
    # print(genres)
    if genres:
        for genre in genres:
            genre_text = genre.text
            print(genre_text)
    else:
        print("No genres")

for id in range(10):
    try:
        id += 1

        url = f'https://tululu.org/txt.php?id={id}'
        title = get_title(id)
        filename = f'{id}. {title}'
        # download_txt(url, filename)

        url = f'https://tululu.org/b{id}/'
        filename = f'{id}'
        # download_image(url, filename)
        # get_comments(url)
        get_genre(url)
    except requests.HTTPError:
        print('Not found book')
