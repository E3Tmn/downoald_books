from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server
from more_itertools import chunked
from pathlib import Path
import os


def on_reload():
    with open('books_json', 'r', encoding='utf-8') as my_file:
        books = json.loads(my_file.read())

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    chunked_books = list(chunked(books, 20))
    template = env.get_template('template.html') 
    name_folder = 'pages'
    for num, books in enumerate(chunked_books):  
        rendered_page = template.render(
            books=list(chunked(books, 2)),
            page_number = num,
            page_amount=len(chunked_books)
        )
        Path(name_folder).mkdir(exist_ok=True)
        with open(os.path.join(name_folder, f'{num+1}index.html'), 'w', encoding='utf-8') as file:
            file.write(rendered_page)


def main():
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == "__main__":
    main()