from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = TextAreaField("Название", validators=[DataRequired()])
    members = TextAreaField("Участники", validators=[DataRequired()])
    email = TextAreaField("Почта", validators=[DataRequired()])
    submit = SubmitField('Применить', validators=[DataRequired()])



