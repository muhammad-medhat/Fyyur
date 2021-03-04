import os
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json


db_name='fyyur'
db_path = f'postgres://postgres:1111@localhost:5432/{db_name}'

db = SQLAlchemy()

'''
setup_db(app)
Binds the flask application with the sqlclemy service
'''
def setup_db(app, db_path=db_path):
    SECRET_KEY = 'secret'
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app=app
    db.init_app(app)    
    mg=Migrate(app, db)
    db.create_all()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
shows=db.Table('shows',   
                
    db.Column('show_id', db.Integer, primary_key=True),
    db.Column('venue_id', db.Integer, db.ForeignKey('venues.id')),
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.id')),
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
    
    # ------------------------ CRUD operattions ------------------------------------
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def  format(self):
        return {
            'id ', self.id,
            'name', self.name,
            'city', self.city,
            'state', self.state,
            'address', self.address,
            'phone', self.phone,
            'image_link ', self.image_link,
            'facebook_link', self.facebook_link
        }

    # ------------------------------------------------------------
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
    # ------------------------ CRUD operattions ------------------------------------
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def  format(self):
        return {
            'id ', self.id,
            'name', self.name,
            'city', self.city,
            'state', self.state,
            'address', self.address,
            'phone', self.phone,
            'image_link ', self.image_link,
            'facebook_link', self.facebook_link
        }

    # ------------------------------------------------------------
    
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
            return []
        else:
            return []