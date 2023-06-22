from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired,Email


class RegisterUserForm(FlaskForm):
    username = wtforms.StringField('Username', validators=[DataRequired()])
    email= wtforms.StringField(validators=[DataRequired(),Email(check_deliverability=True)])
    phone=wtforms.IntegerField(validators=[DataRequired()])
    first_name=wtforms.StringField('First Name',validators=[DataRequired()])
    last_name=wtforms.StringField('Last Name',validators=[DataRequired()])
    password=wtforms.PasswordField(validators=[DataRequired()])
    confirm_password=wtforms.PasswordField("Confirm Password",validators=[DataRequired()])
    submit=wtforms.SubmitField('Register')


class LoginUserForm(FlaskForm):
    email= wtforms.StringField(validators=[DataRequired(),Email(check_deliverability=True)])
    password=wtforms.PasswordField(validators=[DataRequired()])


class CheckEmailForm(FlaskForm):
    email= wtforms.StringField(validators=[DataRequired(),Email(check_deliverability=True)])


class ResetPasswordForm(FlaskForm):
    password=wtforms.PasswordField(validators=[DataRequired()])
    confirm_pass=wtforms.PasswordField("Confirm Password",validators=[DataRequired()])
   
    

    