import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
from urllib.parse import urlsplit
from urllib.parse import urlencode
import argparse
from time import sleep
import json


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def save_book(url, filename, number, folder='books/'):
    params = {'id' : number}
    os.makedirs('books', exist_ok=True)
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)
    filepath = os.path.join(f'{folder}{sanitize_filename(filename)}.txt')
    with open(filepath, 'wb') as file:
        file.write(response.content)


def save_pic(url, folder='covers/'):
    filename = urlsplit(url).path.split('/')[-1]
    os.makedirs('covers', exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    filepath = os.path.join(f'{folder}{sanitize_filename(filename)}')
    with open(filepath, 'wb') as file:
        file.write(response.content)


def get_book_link(start_id, end_id):
    books_list =[]
    text_id = []
    for number in range(start_id,end_id):
        url =f"https://tululu.org/l55/{number}"
        response = requests.get(url)
        response.raise_for_status()
        check_for_redirect(response)
        soup = BeautifulSoup(response.text, 'lxml')
        books_selector = "table.d_book"
        books = soup.select(books_selector)
        for book in books:
            link = book.find("a")["href"]
            full_book_url = urljoin(url, link)
            split_link = urlsplit(link).path.split("/")[1]
            text_id.append(split_link)
            books_list.append(full_book_url)
    return books_list, text_id

def parse_book_page(response, url):
    soup = BeautifulSoup(response.text, 'lxml')
    comment_tag_selector = "div.texts span.black"
    comment_tag = soup.select(comment_tag_selector)
    comments_text = [comment.text for comment in comment_tag]
    genre_tag_selector = "span.d_block a"
    genre_tag = soup.select(genre_tag_selector)
    genres_text = [genre.text for genre in genre_tag]
    title_tag = soup.find('h1').text
    title, author = title_tag.split('::')
    pic_tag_selector = "div.bookimage img"
    pic_tag = soup.select_one(pic_tag_selector)['src']
    full_image_url = urljoin(url, pic_tag)
    book_parameters = {'title': title, 'author': author, 'genre': genres_text, 'comments': comments_text, 'image_url': full_image_url}
    return book_parameters


def main():
    parser = argparse.ArgumentParser(description='Загрузка книг из бесплатной онлайн библиотеки. Выберите, сколько книг хотите скачать введя диапазон id.')
    parser.add_argument("--start_id", default=1, help='id первой книги', type=int)
    parser.add_argument("--end_id", default=10, help='id последней книги', type=int)
    args = parser.parse_args()
    books_link, id_links = get_book_link(args.start_id, args.end_id)
    all_book_parameters = []
    for book_link, id_link in zip(books_link, id_links):
        try: 
            response = requests.get(book_link)
            check_for_redirect(response)
            response.raise_for_status()
            parsed_book_parameters = parse_book_page(response, book_link)
            all_book_parameters.append(parsed_book_parameters)
            full_image_url = parsed_book_parameters['image_url']
            save_pic(full_image_url)
            title = parsed_book_parameters['title']
            filename_book = title.strip()
            text_url = 'https://tululu.org/txt.php'
            save_book(text_url, filename_book, id_link[1:])
            
        except requests.exceptions.HTTPError:
            print('Страница не существует')
        except requests.exceptions.ConnectionError:
            print('Не удалось подключиться. Повторное подключение...')
            sleep(15)
    with open('books.json', 'w', encoding='utf8') as json_file:
        json.dump(all_book_parameters, json_file, ensure_ascii=False)

if __name__ == "__main__":
    main()


