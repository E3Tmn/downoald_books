from jinja2 import Environment, FileSystemLoader, select_autoescape
import json


def main():
    with open('books_json', 'r', encoding='utf-8') as my_file:
        books = json.loads(my_file.read())

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


if __name__ == "__main__":
    main()