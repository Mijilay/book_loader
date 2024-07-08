import requests
import os

url = f'https://tululu.org/txt.php?id=32168'
book = requests.get(url)
with open ("book.txt", 'wb') as file:
    file.write(book.content)