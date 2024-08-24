import requests
import os


os.makedirs("books", exist_ok=True)
for id in range(10):
    id += 1
    url = f'https://tululu.org/txt.php?id={id}'
    response = requests.get(url)
    response.raise_for_status() 
    encoding = response.apparent_encoding
    filename = f'books/id{id}.txt'
    with open(filename, 'w', encoding=encoding) as f:
        f.write(response.text)
