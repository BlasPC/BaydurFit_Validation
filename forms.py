from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, SubmitField
from wtforms.validators import DataRequired, Email

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    country = SelectField('Country of Origin', choices=[
        ('Argentine', 'Argentine'),
        ('Brazil', 'Brazil'),
        ('Chile', 'Chile'),
        ('Uruguay', 'Uruguay'),
        ('Paraguay', 'Paraguay')
    ], validators=[DataRequired()])
    question_a = RadioField('Question A (1 to 10)', choices=[(str(i), str(i)) for i in range(1, 11)], validators=[DataRequired()])
    question_b = RadioField('Question B (1 to 10)', choices=[(str(i), str(i)) for i in range(1, 11)], validators=[DataRequired()])
    submit = SubmitField('Register')
