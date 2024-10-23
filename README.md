# Парсер книг с сайта tululu.org

Код с помощью которого можно создать свою мини библиотеку для того чтобы читать книги оффлайн.

### Как установить


Python3 должен быть уже установлен. Затем используйте pip (или pip3, если есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```

### Как запустить проект


Для того чтобы скачивать книги по порядку нужно открыть терминал и написать:

```sh
python parse_tululu_books.py
```

Чтобы скачать книги в определенном диапазоне нужно указать несколько значений:

1. `START_ID`: число с которого нужно начать скачивать книги (по умолчанию 0)
1. `END_ID`: число которым нужно закончить скачивать книги (по умолчанию 10)

Эти значения нужно указывать после запуска проекта:

```sh
python parse_tululu_books.py --start_id значение --end_id значение
```

Чтобы скачать книги с жанром "фантастика" нужно открыть терминал и написать:

```sh
python parse_tululu_category.py
```

На одной странице содержится 25 книг поэтому чтобы скачать определенное количество страниц нужно указать несколько значений:

1. `START_PAGE`: с какой страницы нужно начать скачивать книги (по умолчанию 1)
1. `END_PAGE`: какой страницей нужно закончить скачивать книги (по умолчанию 5)

Эти значения нужно указывать после запуска проекта:

```sh
python parse_tululu_category.py --start_page значение --end_page значение
```

Также для более удобного скачивания можно указать несколько аргументов(аргументы доступны для обоих файлов):

1. `DEST_FOLDER`: папка в которую нужно скачивать все файлы (по умолчанию library)
1. `SKIP_IMGS`: если указать это значение то картинки не будут скачиваться
1. `SKIP_TXT`: если указать это значение то текст не будет скачиваться

Пример:
```sh
python parse_tululu_books.py --start_id 1 --end_id 5 --dest_folder books_library --skip_imgs 
```
```sh
python parse_tululu_category.py --start_page 12 --end_page 15 --dest_folder books_library --skip_imgs --skip_txt 
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).