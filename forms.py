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
    question_a = RadioField('\n\nHow would you rate your level of expertise:', choices=[
        ('1', ' I have very little or no experience.'),
        ('2', 'I have some knowledge but little experience, I would doubt the quality of my measurements.'),
        ('3', 'I have moderate experience, I trust the quality of my measurements.'),
        ('4', ' I have solid experience.'),
        ('5', 'I have a lot of experience.')
    ], validators=[DataRequired()])

    question_b = RadioField('Question B (1 to 5)', choices=[
        ('1', 'Very Unsatisfied'),
        ('2', 'Unsatisfied'),
        ('3', 'Neutral'),
        ('4', 'Satisfied'),
        ('5', 'Very Satisfied')
    ], validators=[DataRequired()])
    
    
    submit = SubmitField('Register')