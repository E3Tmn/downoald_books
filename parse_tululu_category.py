from bs4 import BeautifulSoup
import requests
import time
from urllib.parse import urljoin


def main():
    try:
        url = 'https://tululu.org/l55/'
        response = requests.get(url)
        response.raise_for_status()
        soap = BeautifulSoup(response.text, 'lxml')
        href_tag = soap.find(class_='d_book').find('a')
        href = href_tag['href']
        print(urljoin(url,href))
    except requests.HTTPError:
        print('HTTP error occurred')
    except requests.ConnectionError:
        print("Connection is interrupted")
        time.sleep(300)


if __name__ == "__main__":
    main()