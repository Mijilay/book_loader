import requests
import os
for number in range(1,10):
    url = f'https://tululu.org/txt.php?id={number}'
    book = requests.get(url)
    with open (f"book_id{number}.txt", 'wb') as file:
        file.write(book.content)