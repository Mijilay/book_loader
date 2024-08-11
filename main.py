import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
from urllib.parse import urlsplit, unquote
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--start_id", default=1, help='Cкачать книги без вирусов с обложками и без.')
parser.add_argument("--end_id", default=10)
args = parser.parse_args()
arg_str_1 = int(args.start_id)
arg_str_2 = int(args.end_id)
def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError

def save_book(url, filename, folder='books/'):
    os.makedirs('books', exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    filepath = os.path.join(f'{folder}{sanitize_filename(filename)}.txt')
    with open (filepath, 'wb') as file:
        file.write(response.content)

def save_pic(url, folder='covers/'):
    filename = urlsplit(url).path.split('/')[-1]
    os.makedirs('covers', exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    filepath = os.path.join(f'{folder}{sanitize_filename(filename)}')
    with open (filepath, 'wb') as file:
        file.write(response.content)
def parse_book_page(response, url):
    soup = BeautifulSoup(response.text, 'lxml')
    comment_tag = soup.find_all('div', class_='texts')
    comments_text = [comment.find("span", class_='black').text for
    comment in comment_tag]
    genre_tag = soup.find('span', class_='d_book').find_all('a')
    genres_text = [genre.text for genre in genre_tag]
    title_tag = soup.find('h1').text
    title,author = title_tag.split('::')

    pic_tag = soup.find('div', class_='bookimage').find('img')['src']
    full_image_url = urljoin(url, pic_tag)
    book_parameters = {'title': title, 'author':author, 'genre': genres_text, 'comments': comments_text, 'image_url': full_image_url}
    return book_parameters

for number in range(arg_str_1, arg_str_2):
    try:  
        url_text = f'https://tululu.org/txt.php?id={number}'
        url_read= f'https://tululu.org/b{number}'
        response_url_read = requests.get(url_read)
        response_url_read.raise_for_status()
        response_url_text = requests.get(url_text)
        response_url_text.raise_for_status()
        check_for_redirect(response_url_text)
        title = parse_book_page(response_url_read, url_read)['title']
        filename_book = f'{number}.{title.strip()}'
        full_image_url = parse_book_page(response_url_read, url_read)['image_url']
        save_book(url_text, filename_book)
        save_pic(full_image_url)

        
    except requests.exceptions.HTTPError:
        print('Страница не существует')