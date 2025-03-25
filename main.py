import datetime

from flask import Flask, render_template, redirect, abort, request
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from forms.jobsform import JobsForm
from forms.registerform import RegisterForm
from forms.departmentform import DepartmentForm
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User()
        user.name = form.name.data
        user.about = form.about.data
        user.email = form.email.data
        user.hashed_password = form.hashed_password.data
        user.created_date = datetime.datetime.now()
        db_sess.merge(user)
        db_sess.commit()
        return redirect('/')
    return render_template('registration.html', title='Регистрация',
                           form=form)


@app.route('/')
def home():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template('base.html', jobs=jobs, current_page="")


@app.route('/departments')
def departments():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    return render_template('base.html', departments=departments, current_page="departments")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.team_leader = current_user.id
        jobs.job = form.job.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.start_date = form.start_date.data
        jobs.end_date = form.end_date.data
        jobs.is_finished = form.is_finished.data
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html', title='Добавление работы',
                           form=form, current_page="add_job")


@app.route('/job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.team_leader == current_user.id
                                          ).first()
        if jobs:
            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          (Jobs.team_leader == current_user.id) | (current_user.id == 1)
                                          ).first()
        if jobs:
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html',
                           title='Редактирование работы',
                           form=form, current_page="job/"
                           )


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                      (Jobs.team_leader == current_user.id) | (current_user.id == 1)
                                      ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/add_department', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = Department()
        department.chief = current_user.id
        department.title = form.title.data
        department.members = form.members.data
        department.email = form.email.data
        current_user.departments.append(department)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/departments')
    return render_template('departments.html', title='Добавление департамента',
                           form=form, current_page="add_department")


@app.route('/department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        departments = db_sess.query(Department).filter(Department.id == id,
                                                       Department.chief == current_user.id
                                                       ).first()
        if departments:
            form.title.data = departments.title
            form.members.data = departments.members
            form.email.data = departments.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        departments = db_sess.query(Department).filter(Department.id == id,
                                                       (Department.chief == current_user.id) | (current_user.id == 1)
                                                       ).first()
        if departments:
            departments.title = form.title.data
            departments.members = form.members.data
            departments.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('departments.html',
                           title='Редактирование департамента',
                           form=form, current_page="department/"
                           )


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).filter(Department.id == id,
                                                   (Department.chief == current_user.id) | (current_user.id == 1)
                                                   ).first()
    if departments:
        db_sess.delete(departments)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')
