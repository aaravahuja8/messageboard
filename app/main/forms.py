from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired
from wtforms.widgets.core import TextArea


class SignUpForm(FlaskForm):
    username = StringField("Enter a username: ", validators=[DataRequired()])
    password = PasswordField("Enter a password: ", validators=[DataRequired()])
    firstname = StringField("Enter your first name: ", validators=[DataRequired()])
    lastname = StringField("Enter your last name: ", validators=[DataRequired()])
    email = StringField("Enter your email address: ", validators=[DataRequired()])
    submit = SubmitField("Sign Up")

class SignInForm(FlaskForm):
    username = StringField("Enter your username: ", validators=[DataRequired()])
    password = PasswordField("Enter your password: ", validators=[DataRequired()])
    rememberme = BooleanField("Keep me logged in")
    submit = SubmitField("Log In")

class SignOutForm(FlaskForm):
    submit = SubmitField("Log Out")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Post Content", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Post")

class CommentForm(FlaskForm):
    content = StringField("Comment", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Comment")

class DeleteForm(FlaskForm):
    submit = SubmitField("Delete Post")