from flask import Flask, redirect, render_template, url_for, request
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
import os
from time import sleep
from datetime import datetime
from pytz import timezone, utc
from flask_mail import Mail, Message
from dotenv import load_dotenv



load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Configure email settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # SMTP server port
app.config['MAIL_USE_TLS'] = True  # Use TLS encryption
app.config['MAIL_USERNAME'] = 'cassandracroan@gmail.com'  # Your email username
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Your email password

mail = Mail(app)


db = SQLAlchemy(app)
Migrate(app,db)

###########
##CLASSES##
###########

class Sighting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String, nullable=True)
    location = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    start_time = db.Column(db.TIMESTAMP, nullable=True)
    created_at = db.Column(db.TIMESTAMP, nullable=True)
    image = db.Column(db.String, nullable=True)
    approval = db.Column(db.String, nullable=True)

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id', name="movie_fk"), nullable=True)
    movie = db.relationship("Movie", foreign_keys=[movie_id], back_populates="sighting")

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column (db.String, nullable=True)
    director = db.Column(db.String, nullable=True)
    studio = db.Column(db.String, nullable=True)
    release_date = db.Column(db.String, nullable=True)
    sighting = db.relationship('Sighting', backref='movie_sighting',
     uselist=False)
    image = db.Column(db.String, nullable=True)



    

##########
##ROUTES##
##########

@app.route('/')
def index():
    sightings = Sighting.query.all()
    return render_template('home.html', sightings=sightings)

@app.route('/movies')
def movies():
    movies = Movie.query.all()
    return render_template('movies.html', movies=movies)

@app.route('/sightings')
def sightings():
    return render_template('sightings.html')

@app.route('/add_sighting', methods=["POST"])
def add_sighting():
    sighting = Sighting()
    sighting.project_name = request.form.get('project_name')
    sighting.location = request.form.get('location')
    sighting.description = request.form.get('description')
    sighting.image = request.form.get('image')

    # CONVERTING TIME TO TO UTC
    date = request.form.get('date')
    hours = request.form.get('hours')
    minutes = request.form.get('minutes')
    ampm = request.form.get('ampm')

    naive_dt = datetime.strptime(f"{date} {hours}:{minutes} {ampm}", '%Y-%m-%d %I:%M %p')
    eastern_tz = timezone('US/Eastern')
    localized_dt = eastern_tz.localize(naive_dt)
    utc_dt = localized_dt.astimezone(utc)

    sighting.start_time = utc_dt

    #GRABBING TIME FOR CREATED_AT
    sighting.created_at = datetime.now()

    db.session.add(sighting)
    db.session.commit()
    
    return redirect("/")


@app.route('/sighting_status')
def sighting_status():
    sightings = Sighting.query.all()
    return render_template('sighting_status.html', sightings=sightings)


@app.route('/add_upcoming', methods=["POST"])
def add_upcoming():
    movie = Movie()
    movie.title = request.form.get('title')
    movie.director = request.form.get('director')
    movie.studio = request.form.get('studio')
    movie.image = request.form.get('image')

    # CONVERTING TIME TO TO UTC
    date = request.form.get('date')
    naive_dt = datetime.strptime(f"{date}", '%Y-%m-%d')
    eastern_tz = timezone('US/Eastern')
    localized_dt = eastern_tz.localize(naive_dt)
    utc_dt = localized_dt.astimezone(utc)

    movie.date = utc_dt

    db.session.add(movie)
    db.session.commit()
    
    return redirect("/")

@app.route('/new_release')
def new_release():
    return render_template('new_release.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Create and send the email
        msg = Message('Contact Form Submission',
                    sender=email,
                    recipients=['cassandracroan@gmail.com'])  # Your email address as the recipient

        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        mail.send(msg)

        return redirect ("/")
    return render_template('contact.html')





if __name__ == '__main__':
    app.run(port=os.getenv('PORT', default=9500), debug=True)







