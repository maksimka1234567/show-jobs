from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    team_leader = TextAreaField('Тимлид', validators=[DataRequired()])
    job = TextAreaField("Описание", validators=[DataRequired()])
    work_size = TextAreaField("Время работы", validators=[DataRequired()])
    collaborators = TextAreaField("Участники", validators=[DataRequired()])
    start_date = TextAreaField("Начало работы", validators=[DataRequired()])
    end_date = TextAreaField("Конец работы", validators=[DataRequired()])
    is_finished = BooleanField("Завершена", validators=[DataRequired()])
    submit = SubmitField('Применить', validators=[DataRequired()])