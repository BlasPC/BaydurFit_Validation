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
    question_a = RadioField('"How experienced do you consider yourself?" (1 to 5)', choices=[
        ('1', 'Very little or no experience'),
        ('2', 'Some knowledge but little experience, unsure of the quality of my measurements'),
        ('3', 'Moderate experience, confident in the quality of my measurements'),
        ('4', 'Solid experience'),
        ('5', 'A lot of experience')
    ], validators=[DataRequired()])
    submit = SubmitField('Register')


    