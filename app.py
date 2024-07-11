from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify
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

from models import User, Result, AccessTime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    if 'file_index' not in session:
        session['file_index'] = 0
    # Log access time
    access_time = AccessTime(user_id=current_user.id, access_time=datetime.utcnow())
    db.session.add(access_time)
    db.session.commit()
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        flash('As part of the Ventilation course at ITBA, we are conducting an analysis of the occlusion test (or Baydur test) used to validate the placement of an esophageal balloon. This is an unpaid academic work.\n\nWe ask for your help by marking the points where you would take measurements to perform the occlusion test.', 'info')  # Flash the message only when accessing the login page directly

    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email.', 'danger')
    return render_template('login.html')



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
        question_b = form.question_b.data

        new_user = User(
            email=email,
            name=name,
            country_of_origin=country,
            question_a=question_a,
            question_b=question_b
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
    file_index = session.get('file_index', 0)
    
    if file_index >= len(file_paths):
        file_index = 0

    filename = file_paths[file_index]
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
        signal3 = df['Ptpulm'][ti*fs:tf*fs]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=signal1, mode='lines', name='Paw[cmH2O]'))
    fig.add_trace(go.Scatter(x=time, y=signal2, mode='lines', name='Pes[cmH2O]'))
    #fig.add_trace(go.Scatter(x=time, y=signal3, mode='lines', name='Ptpulm[cmH2O]'))

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
    new_result = Result(
        user_id=current_user.id,
        time1=data['time1'],
        time2=data['time2'],
        paw1=data['paw1'],
        paw2=data['paw2'],
        pes1=data['pes1'],
        pes2=data['pes2'],
        register_time=datetime.utcnow()
    )
    db.session.add(new_result)
    db.session.commit()
    print(f"Received data: {data}")

    file_index = session.get('file_index', 0)
    file_index = (file_index + 1) % len(get_file_paths())
    session['file_index'] = file_index

    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)