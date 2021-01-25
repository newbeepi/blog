import flask_login
from flask_login import login_user, login_required, logout_user

from . import app, db

from .models import Post, User, Comment
from .forms import PostForm, RegisterForm, LogInForm, CommentForm

from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import check_password_hash, generate_password_hash


@app.route('/')
def index():
    return render_template('index.html', title='Blog')


@app.route('/posts')
def posts():
    return render_template('posts.html', posts=Post.query.all(), title='Posts')


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    form = CommentForm(request.form)
    if request.method == 'POST' and form.validate():
        comment = Comment(form.comment.data, flask_login.current_user.user_id, post_id)
        db.session.add(comment)
        db.session.commit()
        redirect(url_for('post', post_id=post_id))
    return render_template('post.html', post=Post.query.get(post_id), title=Post.query.get(post_id), form=form,
                           comments=Comment.query.filter_by(post_id=post_id))


@app.route('/create_post', methods=['POST', 'GET'])
@login_required
def create_post():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        post = Post(post_name=form.post_name._value(), post_text=form.post_text._value(), user_id=flask_login.current_user.user_id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts'))
    return render_template('Create_post.html', form=form, title='Create your post')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LogInForm(request.form)
    login = form.login.data
    password = form.password.data

    if login and password:
        user = User.query.filter_by(username=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page:
                return redirect(url_for('posts'))
            return redirect(next_page)
        else:
            flash('Login or password is not correct')
    else:
        flash('Please fill login and password fields')
    return render_template('login.html', form=form, title='Log in')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_pwd = generate_password_hash(form.password.data)
        user = User(form.login.data, form.email.data, hash_pwd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login_page'))
    return render_template('register.html', form=form, title='Registration')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)
    return response
