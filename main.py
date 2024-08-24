import requests
import os


os.makedirs("books", exist_ok=True)
for id in range(10):
    id += 1
    url = f'https://tululu.org/txt.php?id={id}'
    # print(url)
    response = requests.get(url)
    response.raise_for_status() 
    encoding = response.apparent_encoding
    filename = f'books/id{id}.txt'
    with open(filename, 'w', encoding=encoding) as f:
        f.write(response.text)

# url = "https://dvmn.org/filer/canonical/1542890876/16/"
# filename = 'dvmn.svg'
# with open(filename, 'w') as file:
#     file.write(response.text)