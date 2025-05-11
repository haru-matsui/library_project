import os

from flask import jsonify, send_file
from flask_httpauth import HTTPBasicAuth
from flask_login import current_user
from flask_restful import reqparse, abort, Resource

from data import db_session
from data.books import Book
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('author', required=True)
parser.add_argument('description')
parser.add_argument('cover')
parser.add_argument('text', required=True)

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    session = db_session.create_session()
    user = session.query(User).filter(User.username == username).first()
    if user and user.check_password(password):
        return username
    return None


@auth.error_handler
def auth_error(status):
    return jsonify({'error': 'Access denied'}), status


def abort_if_book_not_found(book_id):
    session = db_session.create_session()
    book = session.query(Book).get(book_id)
    if not book:
        abort(404, message=f"Book {book_id} not found")
    return book


class BookResource(Resource):
    @auth.login_required
    def get(self, book_id):
        """Скачать книгу в формате FB2"""
        book = abort_if_book_not_found(book_id)
        if not os.path.exists(book.text):
            abort(404, message=f"Book file {book_id} not found")

        return send_file(book.text, as_attachment=True, download_name=f"{book.title}.fb2")


class BookListResource(Resource):
    @auth.login_required
    def get(self):
        session = db_session.create_session()
        books = session.query(Book).all()
        return jsonify({'books': [book.to_dict(only=('id', 'title', 'author', 'description')) for book in books]})
