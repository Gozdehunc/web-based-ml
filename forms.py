from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,Length




class RegisterForm(FlaskForm):
    username = StringField("username",validators=[DataRequired(),Length(min=3,max=80)])
    email = StringField("email",validators=[DataRequired(),Email()])
    password = PasswordField("password",validators=[DataRequired(),Length(min=4,max=80)])
    submit = SubmitField("register")


class LoginForm(FlaskForm):
    username = StringField("username",validators=[DataRequired(),Length(min=3,max=80)])
    password = PasswordField("password",validators=[DataRequired(),Length(min=4,max=80)])
    submit = SubmitField("login")
