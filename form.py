from wtforms import Form,StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import Users

# Register Form Class
class RegisterForm(Form):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')
    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

