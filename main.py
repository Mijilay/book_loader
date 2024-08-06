import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
from urllib.parse import urlsplit, unquote


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

def save_pic(url, filename, folder='covers/'):
    os.makedirs('covers', exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    filepath = os.path.join(f'{folder}{sanitize_filename(filename)}')
    with open (filepath, 'wb') as file:
        file.write(response.content)

for number in range(1,11):
    try:  
        url_text = f'https://tululu.org/txt.php?id={number}'
        url_read= f'https://tululu.org/b{number}'
        response_url_read = requests.get(url_read)
        response_url_read.raise_for_status()
        response_url_text = requests.get(url_text)
        response_url_text.raise_for_status()
        check_for_redirect(response_url_text)
        soup = BeautifulSoup(response_url_read.text, 'lxml')
        comment_tag = soup.find_all('div', class_='texts')
        comments_text = [comment.find("span", class_='black').text for
        comment in comment_tag]
        print(comments_text)
        genre_tag = soup.find('span', class_='d_book').find_all('a')
        genres_text = [genre.text for genre in genre_tag]
        print(genres_text)
        title_tag = soup.find('h1').text
        title,author = title_tag.split('::')
        filename_book = f'{number}.{title.strip()}'
        save_book(url_text, filename_book)
        pic_tag = soup.find('div', class_='bookimage').find('img')['src']
        full_image_url = urljoin(url_read, pic_tag)
        image_name_ext = (pic_tag.split('/'))[2]
        splited_url = urlsplit(full_image_url)
        scheme, netloc, path, query, fragment = (splited_url)
        filename = urlsplit(full_image_url).path.split('/')[-1]
        print(filename)
        save_pic(full_image_url, filename)
        

        
    except requests.exceptions.HTTPError:
        print('Страница не существует')
# for number in range(1,11):
#     try:
#         url_read= f'https://tululu.org/b{number}'
#         response_url_read = requests.get(url_read)
#         response_url_read.raise_for_status()
#         check_for_redirect(response_url_text)
#         soup = BeautifulSoup(response_url_read.text, 'lxml')
#         pic_tag = soup.find('div', class_='bookimage').find('img')['src']
#         full_image_url = urljoin(url_read, pic_tag)
#         image_name_ext = (pic_tag.split('/'))[2]
#         # imagename,ext = (image_name_ext.split('/'))
#         splited_url = urlsplit(full_image_url)
#         scheme, netloc, path, query, fragment = (splited_url)
#         print(splited_url)
#         filename = urlsplit(full_image_url).path.split('/')[-1]
#         print(filename)
#         save_pic(full_image_url, filename)
#     except requests.exceptions.HTTPError:
#         print('Страница не существует')