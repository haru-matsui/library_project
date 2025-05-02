from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя',
                           validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Пароль',
                             validators=[DataRequired(), Length(min=6)])
    password_again = PasswordField('Повторите пароль',
                                   validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
