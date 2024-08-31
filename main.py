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


for id in range(10):
    try:
        id += 1

        url = f'https://tululu.org/txt.php?id={id}'
        title = get_title(id)
        filename = f'{id}. {title}'
        download_txt(url, filename)

        url = f'https://tululu.org/b{id}/'
        filename = f'{id}'
        download_image(url, filename)
        
    except requests.HTTPError:
        print('Not found book')
