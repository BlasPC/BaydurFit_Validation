from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, SubmitField
from wtforms.validators import DataRequired, Email
import pycountry

def get_country_choices():
    countries = [(country.alpha_2, country.name) for country in pycountry.countries]
    return sorted(countries, key=lambda x: x[1])  # Sort by country name

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    country = SelectField('Country of Origin', choices=get_country_choices(), validators=[DataRequired()])
    question_a = RadioField('"How experienced do you consider yourself?" (1 to 5)', choices=[
        ('1', 'Very little or no experience'),
        ('2', 'Some knowledge but little experience, unsure of the quality of my measurements'),
        ('3', 'Moderate experience, confident in the quality of my measurements'),
        ('4', 'Solid experience'),
        ('5', 'A lot of experience')
    ], validators=[DataRequired()])
    submit = SubmitField('Register')
