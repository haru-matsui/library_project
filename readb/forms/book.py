from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField


class UploadBookForm(FlaskForm):
    fb2_file = FileField('FB2 файл книги', validators=[FileRequired()])
    submit = SubmitField('Добавить книгу')
