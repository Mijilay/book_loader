import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
from urllib.parse import urlsplit
from urllib.parse import urlencode
import argparse


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


def parse_book_page(response, url):
    soup = BeautifulSoup(response.text, 'lxml')
    comment_tag = soup.find_all('div', class_='texts')
    comments_text = [comment.find("span", class_='black').text for comment in comment_tag]
    genre_tag = soup.find('span', class_='d_book').find_all('a')
    genres_text = [genre.text for genre in genre_tag]
    title_tag = soup.find('h1').text
    title, author = title_tag.split('::')
    pic_tag = soup.find('div', class_='bookimage').find('img')['src']
    full_image_url = urljoin(url, pic_tag)
    book_parameters = {'title': title, 'author': author, 'genre': genres_text, 'comments': comments_text, 'image_url': full_image_url}
    return book_parameters


def main():
    parser = argparse.ArgumentParser(description='Загрузка книг из бесплатной онлайн библиотеки. Выберите, сколько книг хотите скачать введя диапазон id.')
    parser.add_argument("--start_id", default=1, help='id первой книги', type=int)
    parser.add_argument("--end_id", default=10, help='id последней книги', type=int)
    args = parser.parse_args()

    for number in range(args.start_id, args.end_id):
        try:
            
            
            url = f'https://tululu.org/b{number}/'
            response = requests.get(url)
            check_for_redirect(response)
            response.raise_for_status()
            parsed_book_parameters = parse_book_page(response, url)
            full_image_url = parsed_book_parameters['image_url']
            save_pic(full_image_url)
            title = parsed_book_parameters['title']
            filename_book = f'{number}.{title.strip()}'
            text_url = f'https://tululu.org/txt.php'
            save_book(text_url, filename_book, number)
            
        except requests.exceptions.HTTPError:
            print('Страница не существует')
        except requests.exceptions.ConnectionError:
            print('Не удалось подключиться. Повторное подключение...')


if __name__ == "__main__":
    main()
