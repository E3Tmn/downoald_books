from bs4 import BeautifulSoup
import requests
import time
from urllib.parse import urljoin


def find_links(response, url):
    soap = BeautifulSoup(response.text, 'lxml')
    href_tags = soap.find_all(class_='d_book')
    links = [urljoin(url, tag.find('a')['href']) for tag in href_tags]
    return links


def main():
    try:
        url = 'https://tululu.org/l55/'
        response = requests.get(url)
        response.raise_for_status()
        links = find_links(response, url)
        print(links)
    except requests.HTTPError:
        print('HTTP error occurred')
    except requests.ConnectionError:
        print("Connection is interrupted")
        time.sleep(300)


if __name__ == "__main__":
    main()