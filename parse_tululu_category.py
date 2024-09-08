import argparse
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
for number in range(1,10):

    url =f"https://tululu.org/l55/{number}"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    books = soup.find_all('table', class_='d_book')
    for book in books:
        link = book.find("a")["href"]
        full_book_url = urljoin(url, link)
        print(full_book_url)