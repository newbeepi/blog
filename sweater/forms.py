from wtforms import StringField, TextAreaField, DateTimeField, Form, validators, PasswordField


class PostForm(Form):
    post_name = StringField('Your post name', [validators.Length(min=1, max=50)])
    post_text = TextAreaField('Your post text')


class RegisterForm(Form):
    login = StringField('Login')
    email = StringField('Email', [validators.Email()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LogInForm(Form):
    login = StringField('login')
    password = PasswordField('password')


class CommentForm(Form):
    comment = TextAreaField('Leave your comment', [validators.DataRequired()])