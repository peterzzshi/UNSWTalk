from flask import render_template, flash, redirect, url_for, request
from app import app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


from app.forms import LoginForm, RegistrationForm
from app.models import Student


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.jinja2', title='home page')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        student = Student.get_by_email(email=form.email.data)
        flash('Login requested for user {}, password {}, remember_me={}'.format(
            form.email.data, form.password.data, form.remember_me.data))

        if student is None or not student.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(student, remember=form.remember_me.data)

        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.jinja2', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        _id = form.zid.data
        email = form.email.data
        password = form.password.data
        full_name = form.full_name.data
        birthday = form.birthday.data.strftime("%Y-%m-%d")
        student = Student(_id, email, password, full_name, birthday)

        student.save_to_mongo()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.jinja2', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))