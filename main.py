import requests
import os
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup


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


for id in range(10):
    try:
        id += 1
        url = f'https://tululu.org/txt.php?id={id}'
        title = get_title(id)
        download_txt(url, title)
    except requests.HTTPError:
        print('Not found book')
