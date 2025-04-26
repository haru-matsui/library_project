from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Электронная библиотека</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }
        header {
            background-color: #2c3e50;
            padding: 15px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        nav {
            display: flex;
            justify-content: center;
            max-width: 1200px;
            margin: 0 auto;
        }
        .nav-button {
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            margin: 0 10px;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        .nav-button:hover {
            background-color: #34495e;
        }
        .container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
        }
        .book-day {
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-top: 30px;
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="index.html" class="nav-button">Главная</a>
            <a href="catalog.html" class="nav-button">Каталог</a>
            <a href="book-of-day.html" class="nav-button">Книга дня</a>
            <a href="favorites.html" class="nav-button">Избранное</a>
            <a href="login.html" class="nav-button">Вход/Регистрация</a>
        </nav>
    </header>
</body>
</html>"""


if __name__ == '__main__':
    app.run()
