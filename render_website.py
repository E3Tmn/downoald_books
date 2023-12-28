from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server
from more_itertools import chunked


def on_reload():
    with open('books_json', 'r', encoding='utf-8') as my_file:
        books = json.loads(my_file.read())

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')    
    rendered_page = template.render(
        books=list(chunked(books, 2))
    )
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(rendered_page)


def main():
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='./index.html')


if __name__ == "__main__":
    main()