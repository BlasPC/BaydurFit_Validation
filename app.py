from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from forms import RegistrationForm
import plotly.graph_objs as go
import pandas as pd
import json
import plotly
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from models import User, Result

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    if 'file_index' not in session:
        session['file_index'] = 0
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    welcome_message = "In the context of the Ventilation course at ITBA, we are conducting an analysis of the occlusion test evaluation (or Baydur test) used to validate the placement of an esophageal balloon. This is an unpaid academic work. \nWe ask for your help by marking the points where you would take measurements for the occlusion test."
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email.', 'danger')
    return render_template('login.html', welcome_message=welcome_message)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('file_index', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        country = form.country.data
        question_a = form.question_a.data

        new_user = User(
            email=email,
            name=name,
            country_of_origin=country,
            question_a=question_a
        )

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

def get_file_paths():
    with open('routes.txt') as f:
        return [os.path.join(app.root_path, line.strip()) for line in f]

@app.route('/get_plot')
@login_required
def get_plot():
    file_paths = get_file_paths()
    signal_line = current_user.signal_line  # Use signal_line from user model

    if signal_line >= len(file_paths):
        signal_line = 0

    filename = file_paths[signal_line]
    df = pd.read_csv(filename, sep='\t', skiprows=5)

    time = df['Time']
    signal1 = df['Paw']
    signal2 = df['Pes']
    signal3 = df['Ptpulm']
    cut = True
    if cut:
        ti = 400
        tf = 460
        fs = 256
        time = df['Time'][ti*fs:tf*fs]
        signal1 = df['Paw'][ti*fs:tf*fs]
        signal2 = df['Pes'][ti*fs:tf*fs]
        #signal3 = df['Ptpulm'][ti*fs:tf*fs]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=signal1, mode='lines', name='Paw[cmH2O]'))
    fig.add_trace(go.Scatter(x=time, y=signal2, mode='lines', name='Pes[cmH2O]'))
    fig.add_trace(go.Scatter(x=time, y=signal3, mode='lines', name='Ptpulm[cmH2O]'))

    fig.update_layout(
        title='Respiratory Signals',
        xaxis_title='Time',
        yaxis_title='[cmH2O]',
        dragmode='select',
    )

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route('/receive_data', methods=['POST'])
@login_required
def receive_data():
    data = request.get_json()
    file_paths = get_file_paths()
    
    if current_user.signal_line >= len(file_paths):
        current_user.signal_line = 0
        db.session.commit()
    
    try:
        file_name = file_paths[current_user.signal_line]
    except IndexError:
        return jsonify(success=False, message="Invalid signal line index"), 500

    new_result = Result(
        user_id=current_user.id,
        time1=data['time1'],
        time2=data['time2'],
        paw1=data['paw1'],
        paw2=data['paw2'],
        pes1=data['pes1'],
        pes2=data['pes2'],
        register_time=datetime.utcnow(),
        signal_line=current_user.signal_line,  # Save the current signal line
        file_name=file_name  # Save the file name (or index)
    )
    db.session.add(new_result)
    
    # Update the user's signal line
    current_user.signal_line = (current_user.signal_line + 1) % len(file_paths)  # Move to the next file in routes.txt
    db.session.commit()
    print(f"Received data: {data}")

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
