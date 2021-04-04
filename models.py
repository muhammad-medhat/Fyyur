import os
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

db = SQLAlchemy()

'''
setup_db(app)
Binds the flask application with the sqlclemy service
'''
def setup_db(app):

    app.config.from_object('config')
    db.app=app
    db.init_app(app)    
    mg=Migrate(app, db)
    db.create_all()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    genres = db.Column(ARRAY(db.String()))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(120))
    
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()

    def update(self):
        try:
            print(self.id)
            db.session.commit()
        except:
            db.session.rollback()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
    
    # check has shows function
    def has_shows(self):
        return len(self.get_shows()) >= 0
    
    def format(self):
        return {
            "id": self.id,
            "name": self.name, 
            "city": self.city, 
            "state": self.state,
            "address": self.address, 
            "phone": self.phone, 
            "image_link": self.image_link,
            "facebook_link": self.facebook_link, 
            "genres": self.genres, 
            "website ": self.website , 
            "seeking_talent": self.seeking_talent, 
            "seeking_description ": self.seeking_description
    }


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))

    genres = db.Column(ARRAY(db.String()))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(120))
    
    def insert(self):
        print('============= INSERT ===========')
        try:
            db.session.add(self)
            db.session.commit()
            print('============= INSERT OK===========')
        except:
            db.session.rollback()
            print('============= INSERT error===========')

    def update(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()

    def delete(self):
        print('==== artist delete ============')
        
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            print('==== error delete ============')
            print(dir(db.session))
            print('=======================================')
            db.session.rollback()

    def format(self):
        return {
            "id": self.id,
            "name": self.name, 
            "city": self.city, 
            "state": self.state,
            "address": self.address, 
            "phone": self.phone, 
            "image_link": self.image_link,
            "facebook_link": self.facebook_link, 
            "genres": self.genres, 
            "website ": self.website , 
            "seeking_talent": self.seeking_talent, 
            "seeking_description ": self.seeking_description
    }    
    # check has shows function
    def has_shows(self):
        return len(self.get_shows()) >= 0
    
    def get_shows(self, sh='al'):
        return []


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)    
    start_time = db.Column(db.DateTime)

    artist = db.relationship('Artist', backref=db.backref('shows'))
    
    def insert(self):
        
        print('==== INSERT SHOW ===')
        print(self)
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()   