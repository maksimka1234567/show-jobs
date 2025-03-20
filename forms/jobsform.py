from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms import BooleanField, SubmitField, DateTimeField
from wtforms.validators import DataRequired
import datetime


class JobsForm(FlaskForm):
    team_leader = TextAreaField('Тимлид', validators=[DataRequired()])
    job = TextAreaField("Описание", validators=[DataRequired()])
    work_size = TextAreaField("Время работы", validators=[DataRequired()])
    collaborators = TextAreaField("Участники", validators=[DataRequired()])
    start_date = DateTimeField("Начало работы", default=datetime.datetime.now())
    end_date = DateTimeField("Конец работы", default=datetime.datetime.now())
    is_finished = BooleanField("Завершена", validators=[DataRequired()])
    submit = SubmitField('Применить', validators=[DataRequired()])