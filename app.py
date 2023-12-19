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
    description = db.Column(db.String, nullable=True)
    start_time = db.Column(db.TIMESTAMP, nullable=True)
    created_at = db.Column(db.TIMESTAMP, nullable=True)
    image = db.Column(db.String, nullable=True)
    approval = db.Column(db.String, nullable=True)

    # string location fallback
    location = db.Column(db.String, nullable=True)
    location_lat = db.Column(db.Float, nullable=True)
    location_long = db.Column(db.Float, nullable=True)

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id', name="movie_fk"), nullable=True)
    movie = db.relationship("Movie", foreign_keys=[movie_id], back_populates="sightings")

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column (db.String, nullable=True)
    director = db.Column(db.String, nullable=True)
    studio = db.Column(db.String, nullable=True)
    release_date = db.Column(db.String, nullable=True)
    sightings = db.relationship('Sighting', back_populates='movie')
    image = db.Column(db.String, nullable=True)



    

##########
##ROUTES##
##########

@app.route('/')
def index():
    sightings = Sighting.query.all()
    current_date = datetime.utcnow() 
    return render_template('home.html', sightings=sightings, current_date=current_date)

@app.route('/movies')
def movies():
    movies = Movie.query.all()
    return render_template('movies.html', movies=movies)


@app.route('/about')
def about():
    return render_template('about.html')


#########################
## SUBMIT NEW SIGHTING ##
#########################


@app.route('/submit')
def submit_get():
    return render_template('submit.html')


@app.route('/submit', methods=["POST"])
def submit_post():
    sighting = Sighting()
    sighting.location = request.form.get('location')
    sighting.image = request.form.get('image')

    # GRABBING TIME FOR CREATED_AT
    sighting.created_at = datetime.now()

    db.session.add(sighting)
    db.session.commit()

    # Get the ID of the newly created poster
    new_sighting_id = sighting.id

    msg = Message('**NEW Movie Poster Submission!!**', sender=('Movie Spotter Admin', 'ccrpalmbeach@gmail.com'),
                recipients=['cassandracroan@gmail.com'])  # Your email address as the recipient

    msg.body = f"A new movie poster has been submitted!\n\nApprove the sighting here:\nhttps://moviespotters.com/sighting_status\n\nView Image Here:\n{sighting.image}"

    mail.send(msg)
    
    return redirect(url_for('submit_by_sighting_id_get', sighting_id=new_sighting_id))

@app.route('/submit/<int:sighting_id>')
def submit_by_sighting_id_get(sighting_id):
    # Retrieve the poster from the database using the sighting_id
    sighting = Sighting.query.get_or_404(sighting_id)

    return render_template('submit_by_sighting_id.html',
        hour_numbers=range(1, 13),
        default_hour=6,
        sighting=sighting
    )

#Updates submission to include info from submission_form (second step in submitting a poster)
@app.route('/submit/<int:sighting_id>', methods=["POST"])
def submit_by_sighting_id_post(sighting_id):
    sighting = Sighting.query.get_or_404(sighting_id)

    # copy from form submission to database row
    sighting.project_name = request.form.get('project_name')
    sighting.description = request.form.get('description')

    # CONVERTING TIME TO UTC
    date = request.form.get('date')
    hours = request.form.get('hours')
    minutes = request.form.get('minutes')
    ampm = request.form.get('ampm')

    naive_dt = datetime.strptime(f"{date} {hours}:{minutes} {ampm}", '%Y-%m-%d %I:%M %p')
    eastern_tz = timezone('US/Eastern')
    localized_dt = eastern_tz.localize(naive_dt)
    utc_dt = localized_dt.astimezone(utc)

    sighting.start_time = utc_dt

    db.session.commit()
    return redirect(url_for('submission_confirmation',  sighting_id=sighting_id))

@app.route('/submission_confirmation/<int:sighting_id>', methods=["GET"])
def submission_confirmation(sighting_id):
    sighting = Sighting.query.get(sighting_id)
    return render_template('submission_confirmation.html', sighting=sighting)

#######################################################
##CUSTOM FILTERS FOR TIMEZONE NONSENSE, used in Jinja##
#######################################################

@app.template_filter('convert_timezone')
def convert_timezone(value, tz_from, tz_to):
    # Convert the value from `tz_from` timezone to `tz_to` timezone
    tz_from = timezone(tz_from)
    tz_to = timezone(tz_to)
    localized_dt = tz_from.localize(value)
    converted_dt = localized_dt.astimezone(tz_to)
    return converted_dt

@app.template_filter('strftime')
def strftime_filter(value, format_string):
    return value.strftime(format_string)

################
##ADD SIGHTING##
################


@app.route('/sighting/<int:number>', methods=["GET"])
def view_sighting(number):
    sighting = Sighting.query.get(number)
    movies = Movie.query.all()
    return render_template('sighting.html', sighting=sighting, movies=movies, number=sighting.id)



@app.route('/sighting_status')
def sighting_status():
    sightings = Sighting.query.all()
    movies = Movie.query.all()
    return render_template('sighting_status.html', sightings=sightings, movies=movies)

#Updates sighting status to "Yes" or "No" from button click
@app.route('/update_sighting', methods=["POST"])
def update_sighting():
    sighting_id = request.form.get('sighting_id')
    new_status = request.form.get('status')
    new_project_name = request.form.get('project_name')
    new_location = request.form.get('location')
    new_date = request.form.get('date')
    new_description = request.form.get('description')


    print(f"Sighting ID: {sighting_id}")
    print(f"New Status: {new_status}")
    print(f"New Project Name: {new_project_name}")
    print(f"New Location: {new_location}")
    print(f"New Date: {new_date}")
    print(f"New Description: {new_description}")

    sighting = Sighting.query.get(sighting_id)
    if sighting:
        sighting.approval = new_status
        sighting.project_name = new_project_name
        sighting.location = new_location
        sighting.date = new_date
        sighting.description = new_description
        db.session.commit()
    
    return redirect(url_for('view_sighting', number=sighting.id))




############################
##UPCOMING RELEASE SECTION##
############################

@app.route('/add_upcoming', methods=["POST"])
def add_upcoming():
    movie = Movie()
    movie.title = request.form.get('title')
    movie.director = request.form.get('director')
    movie.studio = request.form.get('studio')
    movie.image = request.form.get('image')
    movie.date = request.form.get('date')

    db.session.add(movie)
    db.session.commit()
    
    return redirect("/movies")

@app.route('/new_release')
def new_release():
    return render_template('new_release.html')


@app.route('/movie/<int:number>', methods=["GET"])
def view_movie(number):
    movie = Movie.query.get_or_404(number)
    sightings = Sighting.query.all()
    return render_template('movie.html', sightings=sightings, movie=movie, number=movie.id)

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







