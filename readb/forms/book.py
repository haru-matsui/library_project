from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField, StringField


class UploadBookForm(FlaskForm):
    fb2_file = FileField('FB2 файл книги', validators=[FileRequired()])
    submit = SubmitField('Добавить книгу')


class SearchForm(FlaskForm):
    search_query = StringField('Поиск')
    submit = SubmitField('Найти')
