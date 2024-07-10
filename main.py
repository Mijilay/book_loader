import requests

for number in range(1,10):
    url = f'https://tululu.org/txt.php?id={number}'
    response = requests.get(url)
    response.raise_for_status()
    with open (f"/books/book_id{number}.txt", 'wb') as file:
        file.write(response.content)