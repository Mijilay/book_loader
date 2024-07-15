import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError

def save_txt(url, filename, folder='books/'):
    os.makedirs('books', exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    filepath = os.path.join(f'{folder}{sanitize_filename(filename)}.txt')
    with open (filepath, 'wb') as file:
        file.write(response.content)

for number in range(1,11):
    try:  
        url_text = f'https://tululu.org/txt.php?id={number}'
        response_url_text = requests.get(url_text)
        response_url_text.raise_for_status()
        check_for_redirect(response_url_text)
        url_read= f'https://tululu.org/b{number}'
        response_url_read = requests.get(url_read)
        response_url_read.raise_for_status()
        soup = BeautifulSoup(response_url_read.text, 'lxml')
        title_tag = soup.find('h1').text
        print(title_tag)
        title,author = title_tag.split('::')
        filename = f'{number}.{title.strip()}'
        save_txt(url_text, filename)
    
        
    except requests.exceptions.HTTPError:
        print('Страница не существует')
