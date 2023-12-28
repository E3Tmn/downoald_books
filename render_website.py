from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server


def on_reload(books):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')    
    rendered_page = template.render(
        books=books
    )
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(rendered_page)


def main():
    with open('books_json', 'r', encoding='utf-8') as my_file:
        books = json.loads(my_file.read())
    on_reload(books)
    server = Server()
    server.serve(root='./index.html')


if __name__ == "__main__":
    main()