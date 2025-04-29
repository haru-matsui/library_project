import os

import chardet
from bs4 import BeautifulSoup
from flask import Flask, render_template_string

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

BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Foliant</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Georgia', serif;
        }}
        body {{
            background-color: #f9f5e9;
            color: #4a3a2a;
            line-height: 1.6;
        }}
        .navbar {{
            background: linear-gradient(135deg, #6d4c41, #8d6e63);
            padding: 1rem 2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-bottom: 1px solid #d7ccc8;
        }}
        .nav-container {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .logo {{
            color: #ffecb3;
            font-size: 1.8rem;
            font-weight: bold;
            text-decoration: none;
            font-family: 'Palatino', serif;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }}
        .nav-links {{
            display: flex;
            gap: 1.5rem;
        }}
        .nav-link {{
            color: #ffecb3;
            text-decoration: none;
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            transition: all 0.3s ease;
            border-bottom: 2px solid transparent;
        }}
        .nav-link:hover {{
            background-color: rgba(255,255,255,0.1);
            border-bottom: 2px solid #ffd54f;
            transform: translateY(-2px);
        }}
        .container {{
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 2rem;
        }}
        {additional_css}
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <a href="/" class="logo">Foliant</a>
            <div class="nav-links">
                <a href="/" class="nav-link">Главная</a>
                <a href="/catalog" class="nav-link">Каталог</a>
                <a href="/book-of-day" class="nav-link">Книга дня</a>
                <a href="/favorites" class="nav-link">Избранное</a>
                <a href="/login" class="nav-link">Вход</a>
            </div>
        </div>
    </nav>
    <div class="container">
        {content}
    </div>
</body>
</html>
"""


@app.route('/')
def index():
    content = """
    <div class="hero">
        <h1>Добро пожаловать в Foliant</h1>
        <p>Уютное пространство для чтения ваших любимых книг</p>
        <div class="decorative-line"></div>
    </div>
    """
    return render_template_string(BASE_TEMPLATE.format(
        title="Главная",
        content=content,
        additional_css="""
        .hero {
            text-align: center;
            padding: 4rem 0;
        }
        .hero h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: #5d4037;
        }
        .hero p {
            font-size: 1.2rem;
            color: #8d6e63;
            margin-bottom: 2rem;
        }
        .decorative-line {
            width: 150px;
            height: 4px;
            background: linear-gradient(90deg, #d7ccc8, #8d6e63);
            margin: 0 auto;
            border-radius: 2px;
        }
        """
    ))


@app.route('/catalog')
def catalog():
    books_list = "\n".join(
        f'<div class="book-card"><a href="/book/{book["id"]}">{book["title"]}</a></div>'
        for book in books_db
    )

    content = f"""
    <h1 class="catalog-title">Каталог книг</h1>
    <div class="book-grid">{books_list}</div>
    """

    return render_template_string(BASE_TEMPLATE.format(
        title="Каталог",
        content=content,
        additional_css="""
        .catalog-title {
            text-align: center;
            margin-bottom: 2rem;
            color: #5d4037;
            font-size: 2rem;
            position: relative;
            padding-bottom: 1rem;
        }
        .catalog-title:after {
            content: "";
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 3px;
            background: #a1887f;
            border-radius: 3px;
        }
        .book-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 2rem;
        }
        .book-card {
            background: #fff8e1;
            border-radius: 8px;
            padding: 1.8rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            border: 1px solid #d7ccc8;
            text-align: center;
        }
        .book-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.12);
            background: #ffecb3;
        }
        .book-card a {
            color: #5d4037;
            text-decoration: none;
            font-weight: 500;
            font-size: 1.1rem;
            display: block;
        }
        .book-card a:hover {
            color: #3e2723;
        }
        """
    ))


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

    content = f"""
    <div class="book-header">
        <h1>{book["title"]}</h1>
        <a href="/catalog" class="back-link">← Вернуться в каталог</a>
    </div>
    <div class="book-content">{text}</div>
    """

    return render_template_string(BASE_TEMPLATE.format(
        title=book["title"],
        content=content,
        additional_css="""
        .book-header {
            margin-bottom: 2.5rem;
            text-align: center;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid #d7ccc8;
        }
        .book-header h1 {
            color: #5d4037;
            margin-bottom: 1rem;
            font-size: 2rem;
        }
        .back-link {
            color: #8d6e63;
            text-decoration: none;
            font-size: 0.95rem;
            transition: all 0.3s ease;
        }
        .back-link:hover {
            color: #5d4037;
            text-decoration: underline;
        }
        .book-content {
            background: #fff8e1;
            padding: 2.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            line-height: 1.8;
            white-space: pre-line;
            font-size: 1.1rem;
            border: 1px solid #d7ccc8;
        }
        .book-content p {
            margin-bottom: 1.5rem;
        }
        """
    ))


if __name__ == '__main__':
    app.run(debug=True)
