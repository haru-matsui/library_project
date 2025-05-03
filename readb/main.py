import base64
import os

import chardet
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, url_for, flash, send_from_directory, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from lxml import etree
from werkzeug.utils import secure_filename

from api import users_api
from data import db_session
from data.books import Book
from data.users import User
from forms.book import UploadBookForm
from forms.user import LoginForm, RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'booky')
app.config['ALLOWED_EXTENSIONS'] = {'fb2'}

os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'bookx'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'covers'), exist_ok=True)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def extract_fb2_metadata(file_path, cover_output):
    with open(file_path, 'rb') as f:
        tree = etree.parse(f)

    ns = {
        'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0',
        'l': 'http://www.w3.org/1999/xlink'
    }

    metadata = {
        'title': None,
        'author': None,
        'description': None,
        'cover': None,
    }

    title_info = tree.xpath('//fb:description/fb:title-info', namespaces=ns)[0]
    metadata['title'] = title_info.xpath('fb:book-title/text()', namespaces=ns)[0]

    author_first = title_info.xpath('fb:author/fb:first-name/text()', namespaces=ns)
    author_last = title_info.xpath('fb:author/fb:last-name/text()', namespaces=ns)
    if author_first or author_last:
        metadata['author'] = ' '.join(filter(None, [
            author_first[0] if author_first else None,
            author_last[0] if author_last else None
        ]))

    description = title_info.xpath('fb:annotation//text()', namespaces=ns)
    if description:
        metadata['description'] = ' '.join(desc.strip() for desc in description if desc.strip())

    cover_href = tree.xpath('//fb:description/fb:title-info/fb:coverpage/fb:image/@l:href', namespaces=ns)
    if cover_href:
        cover_id = cover_href[0].lstrip('#')
        binary_data = tree.xpath(f'//fb:binary[@id="{cover_id}"]/text()', namespaces=ns)
        if binary_data:
            img_data = base64.b64decode(binary_data[0])
            with open(cover_output, 'wb') as img_file:
                img_file.write(img_data)
            metadata['cover'] = os.path.basename(cover_output)

        return metadata

    return metadata


@app.route('/')
def index():
    return render_template('index.html', title="Главная")


@app.route('/catalog')
def catalog():
    db_sess = db_session.create_session()
    books = db_sess.query(Book).all()
    return render_template('catalog.html', title="Каталог", books=books)


@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = UploadBookForm()
    if form.validate_on_submit():
        file = form.fb2_file.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            book_path = os.path.join(app.config['UPLOAD_FOLDER'], 'bookx', filename)
            file.save(book_path)

            cover_name = f"{os.path.splitext(filename)[0]}.jpg"
            cover_path = os.path.join(app.config['UPLOAD_FOLDER'], 'covers', cover_name)

            metadata = extract_fb2_metadata(book_path, cover_path)

            db_sess = db_session.create_session()
            book = Book(
                title=metadata['title'],
                author=metadata['author'],
                description=metadata['description'],
                cover=cover_name,
                text=book_path
            )
            db_sess.add(book)
            db_sess.commit()

            flash('Книга успешно добавлена!', 'success')
        else:
            flash('Недопустимый формат файла. Разрешены только FB2.', 'danger')
    return render_template('add_book.html', title="Добавить книгу", form=form)


@app.route('/book/<int:book_id>')
def read_book(book_id):
    db_sess = db_session.create_session()
    book = db_sess.query(Book).get(book_id)
    if not book:
        return "Книга не найдена", 404

    try:
        with open(book.text, 'rb') as f:
            raw_data = f.read(10000)
            encoding = chardet.detect(raw_data)['encoding']
        with open(book.text, 'r', encoding=encoding) as f:
            fb2_content = f.read()
        soup = BeautifulSoup(fb2_content, 'lxml-xml')
        body = soup.find('body')
        text = body.get_text(separator='\n') if body else "Текст книги не найден."
    except Exception as e:
        text = f"Ошибка при чтении книги: {str(e)}"

    return render_template('book.html', title=book.title, book=book, text=text)


@app.route('/delete_book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    db_sess = db_session.create_session()
    book = db_sess.query(Book).get(book_id)

    if book:
        try:
            if os.path.exists(book.text):
                os.remove(book.text)
            if book.cover and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], 'covers', book.cover)):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'covers', book.cover))
        except Exception as e:
            flash(f'Ошибка при удалении файлов: {str(e)}', 'danger')

        db_sess.delete(book)
        db_sess.commit()
        flash('Книга успешно удалена', 'success')
    else:
        flash('Книга не найдена', 'danger')

    return redirect(url_for('catalog'))


@app.route('/download_book/<int:book_id>')
def download_book(book_id):
    db_sess = db_session.create_session()
    book = db_sess.query(Book).get(book_id)
    if not book or not os.path.exists(book.text):
        flash('Файл книги не найден', 'danger')
        return redirect(url_for('catalog'))

    return send_file(
        book.text,
        as_attachment=True,
        download_name=f"{book.title}.fb2"
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('index'))

        flash("Неверное имя пользователя или пароль", "danger")
        return render_template('login.html', title='Авторизация', form=form)

    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            flash("Пароли не совпадают", "danger")
            return render_template('register.html', title='Регистрация', form=form)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.username == form.username.data).first():
            flash("Такой пользователь уже существует", "danger")
            return render_template('register.html', title='Регистрация', form=form)
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', title='Регистрация', form=form, current_user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/covers/<filename>')
def serve_cover(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'covers'), filename)


def main():
    db_session.global_init("db/users.db")
    app.register_blueprint(users_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
