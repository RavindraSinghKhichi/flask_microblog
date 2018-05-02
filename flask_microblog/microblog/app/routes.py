from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm
from app.models import User
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required


#if imports doesn't work check for the script path is set and app dir is a python package
#microblog dir is set as a source root via make dir as. in right click manu of microblog

@app.route('/', methods=['get'])
@app.route('/index', methods=['get'])
@login_required
def index():
    '''user = {'username': 'Ravindra'}'''
    posts = [{
        'author': {'username': 'Ravindra'},
        'body': 'Beautiful day in Pali!'
    },{
        'author': {'username': 'Bittu'},
        'body': 'Avengers is the movie I am going for.'
    }]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/register', methods=['get', 'post'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('congo, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['get','post'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        #user = None
        if user is None or not user.check_password(form.password.data):
            #flash('Login requested for the user {}, remember_me={}'.format(form.username.data, \
            #                                                           form.remember_me.data))
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        next_page =  request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))