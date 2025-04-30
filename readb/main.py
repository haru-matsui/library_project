import os

import chardet
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)

BOOKS_DIR = os.path.join(os.path.dirname(__file__), "books")

books_db = [
    {"id": 1, "title": "Стивенсон Роберт Луис. Остров сокровищ",
     "filename": "Стивенсон Роберт Луис. Остров сокровищ - TheLib.Ru.fb2"},
    {"id": 2, "title": "Дефо Даниэль. Приключения Робинзона Крузо",
     "filename": "Дефо Даниэль. Приключения Робинзона Крузо - royallib.com.fb2"},
    {"id": 3, "title": "Остап Бендер. Двенадцать стульев",
     "filename": "Ilf_Ostap-Bender_1_Dvenadcat-stulev.-sYjHg.387478.fb2"},
    {"id": 4, "title": "Джек_Лондон. Странник по звездам", "filename": "London_Strannik-po-zvezdam.s9AoWg.468865.fb2"},
    {"id": 5, "title": "Салтыков-Щедрин. История одного города",
     "filename": "Saltykov-Shchedrin_Istoriya-odnogo-goroda.udbxrA.388788.fb2"},
    {"id": 6, "title": "Ремарк. Три товарища", "filename": "Remark_Tri-tovarishcha.Xqb3LQ.253799.fb2"},
]


@app.route('/')
def index():
    return render_template('index.html', title="Главная")


@app.route('/catalog')
def catalog():
    return render_template('catalog.html', title="Каталог", books=books_db)


@app.route('/book/<int:book_id>')
def read_book(book_id):
    book = next((b for b in books_db if b["id"] == book_id), None)
    if not book:
        return "Книга не найдена", 404

    book_path = os.path.join(BOOKS_DIR, book["filename"])

    try:
        with open(book_path, 'rb') as f:
            raw_data = f.read(10000)
            encoding = chardet.detect(raw_data)['encoding']
        with open(book_path, 'r', encoding=encoding) as f:
            fb2_content = f.read()
        soup = BeautifulSoup(fb2_content, 'lxml-xml')
        body = soup.find('body')
        text = body.get_text(separator='\n') if body else "Текст книги не найден."

    except Exception as e:
        text = f"Ошибка при чтении книги: {str(e)}"

    return render_template('book.html', title=book["title"], book=book, text=text)


if __name__ == '__main__':
    app.run(debug=True)
