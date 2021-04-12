import json
from operator import pos
import dateutil.parser
import babel
from flask import (
    Flask,
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for, 
    abort
)
from flask.globals import session
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

import pprint
from sqlalchemy import *
from flask_wtf import FlaskForm as BaseForm
from models import db, Venue, Artist, Show, setup_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)

    def format_datetime(value, format='medium'):
        date = dateutil.parser.parse(value)
        if format == 'full':
            format = "EEEE MMMM, d, y 'at' h:mma"
        elif format == 'medium':
            format = "EE MM, dd, y h:mma"
        return babel.dates.format_datetime(date, format)

    app.jinja_env.filters['datetime'] = format_datetime

    # -----------------------------------------
    # Functions
    # -----------------------------------------
    def get_venue_shows(venue_id, sh='al'):
            # return []
        """
        Function to get shows of this venue
        Args:
            sh (str, optional):
                Defaults to 'all' gets all shows for the selected venue.
            sh (str, optional):
                'nx' gets all next shows for the selected venue.
            sh (str, optional):
                'pv' gets all previous shows for the selected venue.
        """
        venue_shows = []
        if sh == 'nx':
            # GET Upcoming shows
            venue_shows = db.session.query(Show)\
                                    .join(Venue)\
                                    .join(Artist)\
                                    .filter(
                                      Venue.id == venue_id,
                                      Show.start_time > datetime.now()
                                    ).all()

        elif sh == 'pv':
            # GET previous shows
            venue_shows = db.session.query(Show)\
                                    .join(Venue)\
                                    .join(Artist).filter(
                                      Venue.id == venue_id,
                                      Show.start_time < datetime.now()
                                    ).all()
        else:
            # GET all shows
            venue_shows = db.session.query(Show)\
                                    .join(Venue)\
                                    .join(Artist)\
                                    .filter(Venue.id == venue_id).all()
        # print(venue_shows)
        return venue_shows

    def get_artist_shows(artist_id, sh='al'):
            # return []
        """
        Function to get shows of this venue
        Args:
            sh (str, optional):
                Defaults to 'all' gets all shows for the selected venue.
            sh (str, optional):
                'nx' gets all next shows for the selected venue.
            sh (str, optional):
                'pv' gets all previous shows for the selected venue.
        """
        venue_shows = []
        if sh == 'nx':

            # GET Upcoming shows
            artist_shows = db.session.query(Show)\
                                    .join(Venue)\
                                    .join(Artist)\
                                    .filter(
                                      Artist.id == artist_id,
                                      Show.start_time > datetime.now()
                                    ).all()

        elif sh == 'pv':
            # GET previous shows
            venue_shows = db.session.query(Show)\
                                    .join(Venue)\
                                    .join(Artist)\
                                    .filter(
                                      Artist.id == artist_id,
                                      Show.start_time < datetime.now()
                                    ).all()
        else:
            # GET all shows
            venue_shows = db.session.query(Show)\
                                    .join(Venue)\
                                    .join(Artist)\
                                    .filter(
                                      Artist.id == artist_id
                                    ).all()
        return venue_shows

    @app.route('/')
    def index():
          # flash('Fyyur app', category='warning')
          return render_template('pages/home.html')

    #  Venues
    #  ----------------------------------------------------------------

    @app.route('/venues')
    def venues():
        vens = Venue.query.all()
        city_state = db.session.query(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()
        d = []
        for cty, st in city_state:
            vens = Venue.query.filter(Venue.city == cty,
                                      Venue.state == st).all()
            vlist = {}
            for v in vens:
                vlist['city'] = cty
                vlist['state'] = st
                vlist['venues'] = [{
                  'id': v.id,
                  'name': v.name,
                  'num_upcoming_shows': len(get_venue_shows(v.id, 'nx'))
                } for v in vens]
            d.append(vlist)
        return render_template('pages/venues.html', areas=d)

    @app.route('/venues/search', methods=['POST', 'GET'])
    def search_venues():
        search_term = request.form['search_term']
        res = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
        response = {
          "count": len(res),
          "data": [{
            'id': v.id,
            'name': v.name,
            'num_upcoming_shows': get_venue_shows(v.id, 'nx')
            } for v in res]
        }
        return render_template('pages/search_venues.html',
                               results = response,
                               search_term=request.form.get('search_term', ''))

    @app.route('/venues/<int:venue_id>', methods=['GET'])
    def show_venue(venue_id):
      v = Venue.query.get(venue_id)
      data1 = {
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
          "artist_id": s.artist_id,
          "artist_name": Artist.query.get(s.artist_id).name,
          "artist_image_link": Artist.query.get(s.artist_id).image_link,
          "start_time": s.start_time 
          } for s in get_venue_shows(v.id, 'pv')],
        "upcoming_shows": [{
          "artist_id": s.artist_id,
          "artist_name": Artist.query.get(s.artist_id).name,
          "artist_image_link": Artist.query.get(s.artist_id).image_link,
          "start_time": s.start_time
          } for s in get_venue_shows(v.id, 'nx')],
        "past_shows_count": len(get_venue_shows(v.id, 'pv')),
        "upcoming_shows_count": len(get_venue_shows(v.id, 'nx')),
      }
      if v:
          data = v
      else:
          abort(404)
      return render_template('pages/show_venue.html', venue = v)

    #  Create Venue
    #  ----------------------------------------------------------------

    @app.route('/venues/create', methods=['GET'])
    def create_venue_form():
      form = VenueForm()
      return render_template('forms/new_venue.html', form=form)

    @app.route('/venues/create', methods=['POST'])
    def create_venue_submission():

      form = VenueForm()
      # Getting posted data execluding the form token
      post_data = {}
      for k, v in form.data.items():
            if k != 'csrf_token':
              post_data[k] = v
      try:
          if form.validate_on_submit():
            # Setting posted data to the object
            ven = Venue()
            for k, v in post_data.items():
              setattr(ven, k,  v)
            ven.insert()
            # on successful db insert, flash success
            flash(f"Venue  {request.form['name'] } was successfully listed!")
          else:
              flash(f"An error occurred. Venue {request.form['name']}"\
                    "could not be listed.")
      except:
          # on unsuccessful db insert, flash an error instead.
          flash(f"An error occurred. Venue {request.form['name']}"
                + "could not be listed.")
      finally:
          flash(form.errors)
      return redirect(url_for('index'))
    #  Edit Venue
    #  ----------------------------------------------------------------
    @app.route('/venues/<int:venue_id>/edit', methods=['GET'])
    def edit_venue(venue_id):
      flash(f'Editing Veenue: {venue_id}')
      form = VenueForm()
      v = Venue.query.get(venue_id)
      return render_template('forms/edit_venue.html', form=form, venue=v)

    @app.route('/venues/<int:venue_id>/edit', methods=['POST'])
    def edit_venue_submission(venue_id):
      v = Venue.query.get(venue_id)
      form = VenueForm()
      # Getting posted data execluding the form token
      post_data = {}
      for key, val in form.data.items():
          if key != 'csrf_token':
            post_data[key] = val
      try:
        if form.validate_on_submit():
          # Setting posted data to the object
          for key, val in post_data.items():
            setattr(v, key,  val)
          v.update()
          flash(f"Venue  {request.form['name'] } was successfully edited!")
        else:
          flash(f"An error occurred. Venue {request.form['name']}"
                + "could not be edited.")
      except:
        flash(f"An error occurred. Venue {request.form['name']} could not be edited.")

      return redirect(url_for('show_venue', venue_id=venue_id))

    #  Delete Venue
    #  ----------------------------------------------------------------
    @app.route('/venues/<venue_id>', methods=['DELETE'])
    def delete_venue(venue_id):
      try:
        ven = Venue.query.get(venue_id)
        if ven:
          print(ven.has_shows())
          if ven.has_shows():
            flash(f"Venue {ven.name} enrolled in shows",'error')
          else:          
            ven.delete()
            flash("Venue deleted.")
      except:
        flash(f"An error occurred. Venue could not be deleted.", 'error')
      return redirect(url_for('index'))
      return render_template('pages/home.html')
    
    #  Artists
    #  ----------------------------------------------------------------
    @app.route('/artists')
    def artists():
      data = Artist.query.all()
      return render_template('pages/artists.html', artists=data)

    @app.route('/artists/search', methods=['POST'])
    def search_artists():
      search_term = request.form['search_term']
      res = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
      response = {
        "count": len(res), 
        "data": [{'id': a.id, 'name': a.name,
                  'num_upcoming_shows': a.get_shows('nx')} for a in res]
      }
      return render_template('pages/search_artists.html',
                              results=response,
                              search_term=request.form.get('search_term', ''))

    @app.route('/artists/<int:artist_id>')
    def show_artist(artist_id):      
      art = Artist.query.get(artist_id)
      data={
        "id": art.id ,
        "name": art.name,
        "address": art.address,
        "genres": art.genres,
        "city": art.city,
        "state": art.state, 
        "phone": art.phone,
        "website": art.website,
        "facebook_link": art.facebook_link,
        "seeking_talent": art.seeking_talent,
        "seeking_description": art.seeking_description,
        "image_link": art.image_link,
        
        "past_shows": [{
          "venue_id": s.venue_id,
          "venue_name": Venue.query.get(s.venue_id).name ,  
          "venue_image_link": Venue.query.get(s.venue_id).image_link  ,
          "start_time": s.start_time.strftime("%m/%d/%Y, %H:%M")           
          } for s in get_artist_shows(art.id, 'pv')],
        
        "upcoming_shows":  [{
          "venue_id": s.venue_id,
          "venue_name": Venue.query.get(s.venue_id).name ,  
          "venue_image_link": Venue.query.get(s.venue_id).image_link  ,
          "start_time": s.start_time.strftime("%m/%d/%Y, %H:%M")           
          } for s in get_artist_shows(art.id, 'nx')],

        "past_shows_count": len(get_artist_shows(art.id, 'pv')),
        "upcoming_shows_count": len(get_artist_shows(art.id, 'nx'))
      }
      
      return render_template('pages/show_artist.html', artist=data)


    #  Create Artist
    #  ----------------------------------------------------------------

    @app.route('/artists/create', methods=['GET'])
    def create_artist_form():
      form = ArtistForm()
      return render_template('forms/new_artist.html', form=form)

    @app.route('/artists/create', methods=['POST'])
    def create_artist_submission():

      form = ArtistForm()
      # Getting posted data execluding the form token
      post_data = {}
      for k, v in form.data.items():
            if k != 'csrf_token':
              post_data[k] = v
      try:
          if form.validate_on_submit():
            # Setting posted data to the object
            art = Artist()
            for k, v in post_data.items():
              setattr(art, k,  v)
            art.insert()
            # on successful db insert, flash success
            flash(f"Artist  {request.form['name'] } was successfully listed!")
          else:
              flash(f"An error occurred. Artist {request.form['name']} could not be listed.")
      except:
          # on unsuccessful db insert, flash an error instead.
          flash(f"An error occurred. Artist {request.form['name']}"
                + " could not be listed.")
      finally:
          flash(form.errors)
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      return redirect(url_for('index'))

    #  Edit Artist
    #  ----------------------------------------------------------------
    @app.route('/artists/<int:artist_id>/edit', methods=['GET'])
    def edit_artist(artist_id):
      flash(f'Editing Veenue: {artist_id}')
      form = ArtistForm()
      v = Artist.query.get(artist_id)
      return render_template('forms/edit_artist.html', form=form, artist=v)

    @app.route('/artists/<int:artist_id>/edit', methods=['POST'])
    def edit_artist_submission(artist_id):
      v = Artist.query.get(artist_id)
      form = ArtistForm()
      # Getting posted data execluding the form token
      post_data={}
      for key, val in form.data.items():
          if key != 'csrf_token':
            post_data[key] = val
      try :
        if form.validate_on_submit():
          # Setting posted data to the object
          for key, val in post_data.items():
            setattr(v, key,  val)
        
          v.update()
          flash(f"Artist  {request.form['name'] } was successfully edited!")
        else:
          flash(f"An error occurred. Artist {request.form['name']} could not be edited.")
      except:
        flash(f"An error occurred. Artist {request.form['name']} could not be edited.")

      return redirect(url_for('show_artist', artist_id=artist_id))


    #  Delete Artist
    #  ----------------------------------------------------------------
    @app.route('/artists/<artist_id>', methods=['DELETE'])
    def delete_artist(artist_id):
      print('=============== Delete endpoint ===============')
      try:            
        art = Artist.query.get(artist_id)
        if art:
          # print(art)
          if art.has_shows():
            flash(f"Artist {art.name} enrolled in shows",'error' )
          else:          
            art.delete()
            flash("Artist deleted.")
      except:
        flash(f"An error occurred. Artist could not be deleted.", 'error')
      
      return render_template('pages/home.html')



    #  Shows
    #  ----------------------------------------------------------------

    @app.route('/shows')
    def shows():
 
      shows_list = db.session.query(Show)\
          .join(Venue, Show.venue_id == Venue.id)\
          .join(Artist, Show.artist_id == Artist.id)\
          .all()
      ret = [{     
            "venue_id": s.venue_id,
            "venue_name": Venue.query.get(s.venue_id).name,
            "artist_id": s.artist_id,
            "artist_name": Artist.query.get(s.artist_id).name,
            "artist_image_link": Artist.query.get(s.artist_id).image_link,
            "start_time": s.start_time
          } for s in shows_list]
      # print(ret)
      return render_template('pages/shows.html', shows=ret)

    @app.route('/shows/create')
    def create_shows():
      # renders form. do not touch.
      form = ShowForm()
      return render_template('forms/new_show.html', form=form)

    @app.route('/shows/create', methods=['POST'])
    def create_show_submission():
          
      form = ShowForm() 
      post_data = {
          "artist_id"  : form.artist_id.data, 
          "venue_id"   : form.venue_id.data, 
          "start_time" : form.start_time.data
      }
      try :
        if form.validate_on_submit():
          print('after valid')
          sh = Show(
            artist_id  = post_data["artist_id" ],
            venue_id   = post_data["venue_id"  ],
            start_time = post_data["start_time"]
          )
          sh.insert()
          flash('Show was successfully listed!')
      except:
        flash('An error occurred. Show could not be listed.')       
      return render_template('pages/home.html')
    
    #########################Just for testing ##############################
    # @app.route('/venues/add', methods=['POST', 'GET'])
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
    
    return app

