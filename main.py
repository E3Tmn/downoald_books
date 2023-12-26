import requests
from pathlib import Path
from bs4 import BeautifulSoup
import os
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
import argparse
import time
import re
import json


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_picture(count, book_cover_url, book_url):
    ext = os.path.splitext(book_cover_url)[1]
    url = urljoin(book_url, book_cover_url)
    response = requests.get(url)
    response.raise_for_status()
    image_folder = 'image'
    Path(image_folder).mkdir(exist_ok=True)
    with open(os.path.join(image_folder, f'{count}{ext}'), 'wb') as file:
        file.write(response.content)


def download_book(count, book_title, book_folder, id):
    payloads = {
            'id': id
        }
    book_url = f"https://tululu.org/txt.php"
    book_response = requests.get(book_url, params=payloads)
    book_response.raise_for_status()
    check_for_redirect(book_response)
    book_name = f"{book_title}.txt"
    Path(book_folder).mkdir(exist_ok=True)
    with open(os.path.join(book_folder, f'{count}.{book_name}'), 'wb') as file:
        file.write(book_response.content)


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.select_one('head title')
    title_text = title_tag.text.split(' - ')
    genre_tag = soup.select_one('span.d_book a')
    genre = genre_tag['title'].split(' - ')[0]
    picture_url = soup.select_one('div .bookimage a img')['src']
    comments_tag = soup.select('div .texts')
    comments = [comment.select_one('span.black').text for comment in comments_tag]
    return {'book_title': sanitize_filename(title_text[0]),
            'book_author': title_text[1].split(',')[0],
            'book_genre': genre,
            'book_cover_url': picture_url,
            'comments_on_book': comments}    


def main():
    parser = argparse.ArgumentParser(description='''Программа позволяет скачать книги, их обложки и комментарии с сайта https://tululu.org/.
                                     Для начала работы желательно выбрать с какой страницы(start_page) по какую страницу(end_page) скачивать книги''')
    parser.add_argument('--start_page', type=int, default=701, help='Номер первой страницы')
    parser.add_argument('--end_page', type=int, default=702, help='Номер второй страницы')
    parser.add_argument('--dest_folder', default='books', help='Путь к каталогу с результатами парсинга: картинкам, книгам, JSON')
    parser.add_argument('--skip_imgs', action='store_true', help='Выбрав этот параметр Вы подтверждаете отказ от скачивания картинок')
    parser.add_argument('--skip_txt', action='store_true', help='Выбрав этот параметр Вы подтверждаете отказ от скачивания книг')
    args = parser.parse_args()
    start_page = args.start_page
    end_page = args.end_page
    skip_imgs = args.skip_imgs
    skip_txt = args.skip_txt
    dest_folder = args.dest_folder
    count = 0
    books = []
    for page in range(start_page, end_page):  
        try:
            url = f'https://tululu.org/l55/{page}/'
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            soap = BeautifulSoup(response.text, 'lxml')
            href_tags = soap.select('.d_book')
            for tag in href_tags:
                try:
                    book_link = tag.select_one('a')['href']
                    count +=1
                    link = urljoin(url, book_link)    
                    response = requests.get(link)
                    response.raise_for_status()
                    check_for_redirect(response)
                    book = parse_book_page(response)
                    books.append(book)
                    if not skip_txt:
                        download_book(count, book['book_title'], dest_folder, re.findall(r'\d+', book_link)[0])
                    if not skip_imgs:
                        download_picture(count, book['book_cover_url'], link)
                except requests.HTTPError:
                    print('HTTP error occurred')
                except requests.ConnectionError:
                    print('Connection is interrupted')
                    time.sleep(300)
        except requests.HTTPError:
            print('HTTP error occurred')
        except requests.ConnectionError:
            print('Connection is interrupted')
            time.sleep(300)
    with open('books_json', "w", encoding='utf-8') as file:
        file.write(json.dumps(books, ensure_ascii=False))

if __name__ == "__main__":
    main()
