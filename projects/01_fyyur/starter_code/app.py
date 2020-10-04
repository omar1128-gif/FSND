#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from datetime import datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
import sys
from forms import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(),unique=True, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120),unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True)
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    image_link = db.Column(db.String(500) , unique=True)
    website = db.Column(db.String(120), unique=True)
    facebook_link = db.Column(db.String(120), unique=True)
    seeking_talent = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(500))

    shows = db.relationship('Show', backref='venue',lazy=True ,cascade="all,delete")


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True ,nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), unique=True)
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    image_link = db.Column(db.String(500), unique=True)
    website = db.Column(db.String(120), unique=True)
    facebook_link = db.Column(db.String(120), unique=True)
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))

    shows = db.relationship('Show', backref='artist', lazy=True , cascade="all,delete")


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer,primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id', ondelete="CASCADE"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id', ondelete="CASCADE"), nullable=False)
    start_time = db.Column(db.DateTime(), nullable=False)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    venue_query = Venue.query.group_by(Venue.id, Venue.state, Venue.city).all()
    upcoming_shows = []
    city_and_state = ''
    data = []
    for venue in venue_query:
        for show in venue.shows:
            if show.start_time > datetime.now():
                upcoming_shows.append(show)
        if city_and_state == venue.city + venue.state:
            data[len(data) - 1]["venues"].append({
              "id": venue.id,
              "name": venue.name,
              "num_upcoming_shows": len(upcoming_shows)
            })
        else:
            city_and_state = venue.city + venue.state
            data.append({
              "city": venue.city,
              "state": venue.state,
              "venues": [{
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": len(upcoming_shows)
              }]
            })
    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term').strip()
    matches = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
    count =  len(matches)
    response={
        "count": count,
        "data": matches
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

    venue = Venue.query.get(venue_id)
    past_shows = Show.query.filter(Show.venue_id == venue_id).filter(Show.start_time < datetime.now()).all()
    upcoming_shows = Show.query.filter(Show.venue_id == venue_id).filter(Show.start_time > datetime.now()).all()
    upcoming = []
    for show in upcoming_shows:
        upcoming.append({
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
        })
    past = []
    for show in past_shows:
        past.append({
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
        })
    data = {
        "id" : venue_id ,
        'name': venue.name,
        'genres': venue.genres,
        'address': venue.address,
        'city': venue.city,
        'state': venue.state,
        'phone': venue.phone,
        'website': venue.website,
        'facebook_link': venue.facebook_link,
        'image_link': venue.image_link,
        'past_shows': past,
        'upcoming_shows': upcoming,
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    try:
        venue = Venue()
        name = request.form.get('name')
        venue.name = name
        venue.city = request.form.get('city')
        venue.state = request.form.get('state')
        venue.address = request.form.get('address')
        venue.phone = request.form.get('phone')
        venue.genres = request.form.getlist('genres')
        venue.website = request.form.get('website')
        venue.image_link = request.form.get('image_link')
        venue.facebook_link = request.form.get('facebook_link')
        db.session.add(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occured. Venue ' +
                  name + ' Could not be listed!')
        else:
            flash('Venue ' + name +
             ' was successfully listed!')

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    error = False
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
    except Exception as e:
        error = True
        print(f'Error ==> {e}')
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        flash(f'An error occurred. Venue {venue_id} could not be deleted.')
        abort(400)
    else :
        flash(f'Venue {venue_id} was successfully deleted.')

    return redirect(url_for('index'))



#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data = Artist.query.order_by(Artist.id).all()
    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term').strip()
    matches = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
    response = {
        "count": len(matches),
        "data": matches
    }

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    past_shows = Show.query.filter(Show.artist_id == artist_id).filter(Show.start_time < datetime.now()).all()
    upcoming_shows = Show.query.filter(Show.artist_id == artist_id).filter(Show.start_time > datetime.now()).all()
    upcoming = []
    for show in upcoming_shows:
        upcoming.append({
          "venue_id": show.venue_id,
          "venue_name": show.venue.name,
          "venue_image_link": show.venue.image_link,
          "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
        })

    past = []
    for show in past_shows:
        past.append({
          "venue_id": show.artist_id,
          "venue_name": show.venue.name,
          "venue_image_link": show.venue.image_link,
          "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
        })
    data = {
        "id" : artist.id,
        'name': artist.name,
        'genres': artist.genres,
        'city': artist.city,
        'state': artist.state,
        'phone': artist.phone,
        'website': artist.website,
        'facebook_link': artist.facebook_link,
        'image_link': artist.image_link,
        'past_shows': past,
        'upcoming_shows': upcoming,
        'past_shows_count': len(past),
        'upcoming_shows_count': len(upcoming)
    }

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    error = False
    try:
        artist = Artist.query.get(artist_id)
        artist.name = request.form.get('name')
        artist.city = request.form.get('city')
        artist.state = request.form.get('state')
        artist.phone = request.form.get('phone')
        artist.genres = request.form.getlist('genres')
        artist.website = request.form.get('website')
        artist.image_link = request.form.get('image_link')
        artist.facebook_link = request.form.get('facebook_link')
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            print(f'An error occured. Artist with id {artist_id} was not modified')
        else:
            print(f'Artist with id {artist_id} was successfully modified')

    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    error = False
    try:
        venue = Venue.query.get(venue_id)
        venue.name = request.form.get('name')
        venue.city = request.form.get('city')
        venue.state = request.form.get('state')
        venue.address = request.form.get('address')
        venue.phone = request.form.get('phone')
        venue.genres = request.form.getlist('genres')
        venue.website = request.form.get('website')
        venue.image_link = request.form.get('image_link')
        venue.facebook_link = request.form.get('facebook_link')
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            print(f'An error occured. Venue with id {venue_id} was not modified')
        else:
            print(f'Venue with id {venue_id} was successfully modified')
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False
    try:
        artist = Artist()
        name = request.form.get('name')
        artist.name = name
        artist.city = request.form.get('city')
        artist.state = request.form.get('state')
        artist.phone = request.form.get('phone')
        artist.genres = request.form.getlist('genres')
        artist.website = request.form.get('website')
        artist.image_link = request.form.get('image_link')
        artist.facebook_link = request.form.get('facebook_link')
        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occured. Artist ' +
                  name + ' Could not be listed!')
        else:
            flash('Artist ' + name +
                  ' was successfully listed!')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    shows = Show.query.order_by(Show.start_time).all()
    num_shows = len(Show.query.filter(Show.start_time > datetime.now()).all())
    data = []
    for show in shows:
        data.append({
        "venue_id": show.venue.id,
        "venue_name": show.venue.name,
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link ,
        "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
        })


    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False
    date_format = '%Y-%m-%d %H:%M:%S'
    try:
        show = Show()
        show.artist_id = request.form.get('artist_id')
        show.venue_id = request.form.get('venue_id')
        show.start_time = datetime.strptime(request.form.get('start_time'), date_format)
        db.session.add(show)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Show could not be listed.')
        else:
            flash('The show was successfully listed!')

    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
