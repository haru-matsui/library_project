from datetime import datetime

import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Book(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    author = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text)
    cover = sqlalchemy.Column(sqlalchemy.String)  # Путь к обложке
    text = sqlalchemy.Column(sqlalchemy.String)  # Путь к файлу книги
    upload_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'cover': self.cover,
            'text': self.text,
            'upload_date': self.upload_date
        }
