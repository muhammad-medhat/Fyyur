#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from operator import pos
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask.globals import session
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

import pprint
from flask_migrate import Migrate
# from flask import *
from sqlalchemy import *
# from sqlalchemy import String, JSON
from flask_wtf import FlaskForm as BaseForm
# from flask_marshmallow import Marshmallow

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
mg=Migrate(app, db)
# ma = Marshmallow(app)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
shows=db.Table('shows',    
    db.Column('venue_id', db.Integer, db.ForeignKey('venues.id', primary_key=True)),
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.id', primary_key=True)),
    db.Column('start_date', db.DateTime)
)

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(256))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(JSON)
    website = db.Column(db.String(256))
    seeking_talent= db.Column(db.Boolean())
    seeking_description= db.Column(db.String(256))
    artists = db.relationship('Artist', secondary=shows, backref=db.backref('Venue', lazy=True))
    
    def get_shows(self, sh='al'):
      return []
      """
        Function to get shows of this venue
      Args:
          sh (str, optional): Defaults to 'all' gets all shows for the selected venue.
          sh (str, optional): 'nx' gets all next shows for the selected venue.
          sh (str, optional): 'pv' gets all previous shows for the selected venue.
      """

      if sh == 'nx':
        # GET Upcoming shows
        return db.session.query(shows).join(Artist).filter( Venue.id==self.id, shows.start_date>datetime.now()).all()
      elif sh=='pv':
        # GET previous shows
        return db.session.query(shows).join(Artist).filter( Venue.id==self.id, shows.start_date<datetime.now()).all()
      else:
        # GET all shows
        q= db.session.query(shows).join(Artist).filter( Venue.id==self.id)
        print(q)
        return db.session.query(shows).join(Artist).filter( Venue.id==self.id).all()


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

    genres = db.Column(JSON)
    website = db.Column(db.String(256))
    seeking_talent= db.Column(db.Boolean())
    seeking_description= db.Column(db.String(256))
    
    def get_shows(self, sh='al'):
      # return []
      """
        Function to get shows of this venue
      Args:
          sh (str, optional): Defaults to 'all' gets all shows for the selected venue.
          sh (str, optional): 'nx' gets all next shows for the selected venue.
          sh (str, optional): 'pv' gets all previous shows for the selected venue.
      """
      if sh == 'al':
        q= db.session.query(shows).join(Artist).filter( Venue.id==self.id)
        print(q)
        return db.session.query(shows).join(Artist).join(Venue).filter( Venue.id==self.id).all()
      elif sh == 'nx':
        return 0
      else:
          return 0

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
db.create_all()
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

# -----------------------------------------
# Functions
# -----------------------------------------
def get_cities():
      citystate = text("""
          Select distinct city, state
          from venues 
      """)
      return db.engine.execute(citystate)
    
def get_vens_by_city( c_name):
    q = text("""
          Select id, name
          from venues where city=:city
      """)
    return db.engine.execute(q, city=c_name)

def get_venues():
    cities = get_cities()
    for c in cities:
        dict_c = dict(c)

        vens=dict({"Venues": dict(get_vens_by_city(c.city).fetchall())})
    return (dict(dict_c, **vens))
def get_vlist():
      vens=[]
      for c in get_cities():
            vens.append(c)
      return vens

def list_to_string(l):
      return l.join(', ')
  
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
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  vens = Venue.query.all()
  city_state = db.session.query(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()
  d=[]
  for cty, st in city_state:
        vens=Venue.query.filter(Venue.city==cty, Venue.state==st).all()
        vlist={}
        for v in vens:
            vlist['city'] = cty
            vlist['state'] = st
            vlist['venues'] = [{'id':v.id, 'name':v.name, 'num_upcoming_shows': len(v.get_shows('nx'))} for v in vens]
        d.append(vlist)      
  return render_template('pages/venues.html', areas=d)

@app.route('/venues/search', methods=['POST', 'GET'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  search_term = request.form['search_term']
  # q = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))
  res = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()

  response = {
    "count": len(res), 
    "data": [{'id':v.id, 'name':v.name, 'num_upcoming_shows': v.get_shows('nx')} for v in res]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>', methods=['GET'])
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  v = Venue.query.get(venue_id)
  
  data1={
    "id": v.id,
    "name": v.name,
    "genres": v.genres,
    "address": v.address,
    "city": v.city, 
    "state": v.state,
    "phone": v.phone,
    "website": v.website,
    "facebook_link": v.facebook_link,
    "seeking_talent": v.seeking_talent,
    "seeking_description": v.seeking_description, 
    "image_link": v.image_link,
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  print(data1)
  if v:
      data=v
  else:
      return"NO Data"
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=v)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  form = VenueForm()
  
  post_data = {
      "name"          : form.name.data, 
      "city"          : form.city.data, 
      "state"         : form.state.data, 
      "phone"         : form.phone.data, 
      "address"       : form.address.data , 
      "genres"        : form.genres.data , 
      "facebook_link" : form.facebook_link.data 
  }
  print(post_data)
  try :
      if form.validate_on_submit():
        v = Venue(
          name=           post_data['name'],
          city=           post_data['city'],
          state=          post_data['state'],
          phone=          post_data['phone'],
          address=        post_data['address'],
          genres=         getlist(post_data['genres']),
          facebook_link=  post_data['facebook_link']
        )

        db.session.add(v)
        db.session.commit()           
        # on successful db insert, flash success
        flash(f"Venue  {request.form['name'] } was successfully listed!")
      else:
            flash(f"An error occurred. Venue {request.form['name']} could not be listed.")

  except:
      # TODO: on unsuccessful db insert, flash an error instead.
      flash(f"An error occurred. Venue {request.form['name']} could not be listed.")
  finally:
      flash(form.errors)


  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return redirect(url_for('index'))



@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  v = Venue.query.get(venue_id)
  print(v)

  if v:
      try:
          db.session.delete(v)
          db.session.commit()
      except:
          db.session.rollback()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  search_term = request.form['search_term']
  res = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  response = {
    "count": len(res), 
    "data": [{'id':a.id, 'name':a.name, 'num_upcoming_shows': a.get_shows('nx')} for a in res]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  art = Artist.query.get(venue_id)

  data1={}
  #   "id":                  art.id ,
  #   "name":                art.name,
  #   "genres":              art.genres,
  #   "city":                art.city,
  #   "state":               art.state, 
  #   "phone":               art.phone,
  #   "website":             art.website,
  #   "facebook_link":       art.facebook_link,
  #   "seeking_venue":       art.seeking_venue,
  #   "seeking_description": art.seeking_description,
  #   "image_link":          art.image_link,
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The  " ,  
  #       "venue_image_link": "" ,
  #       "start_time": "2019",  
  #   "upcoming_shows": [],    
  #   "past_shows_count": 1,    
  #   "upcoming_shows_count"    
  # }]
  # }]

  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=art)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()  
  artist =  Artist.query.get(artist_id)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  v = Venue.query.get(venue_id)

  venue={
    "id": v.id,
    "name": v.name,
    "genres": v.genres,
    "address": v.address,
    "city": v.city, 
    "state": v.state,
    "phone": v.phone,
    "website": v.website,
    "facebook_link": v.facebook_link,
    "seeking_talent": v.seeking_talent,
    "seeking_description": v.seeking_description, 
    "image_link": v.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm()

  post_data = {
      "name"          : form.name.data, 
      "city"          : form.city.data, 
      "state"         : form.state.data, 
      "phone"         : form.phone.data, 
      "address"       : form.address.data , 
      "genres"        : form.genres.data , 
      "facebook_link" : form.facebook_link.data 
  }
  print(post_data)
  
  try :
      if form.validate_on_submit():
        print('------------ try block validated ------------------------')
        art = Artist(
          name=           post_data['name'],
          city=           post_data['city'],
          state=          post_data['state'],
          phone=          post_data['phone'],
          address=        post_data['address'],
          genres=         post_data['genres'],
          facebook_link=  post_data['facebook_link']
        )
        print('venues')
        print(art)
        db.session.add(art)
        db.session.commit()           
        # on successful db insert, flash success
        flash(f"Artist  {request.form['name'] } was successfully listed!")
      else:
        print("----------------- try not validated-----------------")
  except:
      # TODO: on unsuccessful db insert, flash an error instead.
      flash(f"An error occurred. Artist {request.form['name']} could not be listed.")
  
  
  

  
  
  
  # on successful db insert, flash success
  flash(post_data)
  # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  q = text("""
      select v.id as venue_id , v.name as venue_name, a.id as artist_id, a.name as artist_name, 
      a.image_link as artist_image_link, s.start_date as start_time
      from shows s 
      join venues v on v.id=s.venue_id
      join artists a on a.id=s.artist_id
""")
  res = db.engine.execute(q)
  print(res.__dict__)
  # q1=db.session.query(shows).join(Artist).join(Venue)
  # print(q1)
  
  return render_template('pages/shows.html', shows=res)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')
#######################################################
@app.route('/venues/add', methods=['POST', 'GET'])
def add_vnu():
      try:
        post_data=request
        print(post_data)
        v = Venue(
            name=           post_data['name'],
            city=           post_data['city'],
            state=          post_data['state'],
            phone=          post_data['phone'],
            address=        post_data['address'],
            genres=         post_data['genres'],
            facebook_link=  post_data['facebook_link']
          )
      except Exception as e:
        print('=================================================')
        print(e.__dict__)
        print('=================================================')

        # print(request.__dict__ )
      
      return render_template('forms/add_vnu.html')


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
