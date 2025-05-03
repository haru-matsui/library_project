import os
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
    cover = sqlalchemy.Column(sqlalchemy.String)
    text = sqlalchemy.Column(sqlalchemy.String)
    upload_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)

    def get_file_size(self):
        if os.path.exists(self.text):
            size = os.path.getsize(self.text)
            if size < 1024:
                return f"{size} Б"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} КБ"
            else:
                return f"{size / (1024 * 1024):.1f} МБ"
        return "0 Б"
