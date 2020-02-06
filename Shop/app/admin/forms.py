from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,FileField,TextField
from app.models import User,UserLog
from wtforms.validators import DataRequired,ValidationError,EqualTo,Email

user = User.query.all()

class RegistForm(FlaskForm):
    '用户注册表单'
    account = StringField(
        label = '用户名'

    )