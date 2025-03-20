import datetime

from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = TextAreaField("Имя", validators=[DataRequired()])
    about = TextAreaField("О пользователе", validators=[DataRequired()])
    email = TextAreaField("Почта", validators=[DataRequired()])
    hashed_password = TextAreaField("Пароль", validators=[DataRequired()])
    submit = SubmitField('Применить', validators=[DataRequired()])