# Скачиваем книги с сайта
Программа позволяет скачать книги, их обложки и комментарии с сайта https://tululu.org/
Пример сайта на котором отображаются скачанные книги https://e3tmn.github.io/downoald_books/pages/1index.html
## Зависимости
Python должен быть уже установлен. Для установки необходимым библиотек используйте файл `requirements.text`.
```bash
pip install -r requirements.txt
```
## Запуск
Запуск на Windows.
```bash
python main.py
```
Доступные аргументы:
1. start_page - Номер первой страницы.
2. end_page - Номер второй страницы.
3. dest_folder - Путь к каталогу с результатами парсинга: картинкам, книгам, JSON.
4. skip_imgs - Выбрав этот параметр Вы подтверждаете отказ от скачивания картинок.
5. skip_txt - Выбрав этот параметр Вы подтверждаете отказ от скачивания книг.
   
Пример использования всех этих аргументов:
```bash
python main.py --skip_imgs --dest_folder C:\Users\nikit\Documents\GitHub\books --start_page 2 --end_page 5
```
