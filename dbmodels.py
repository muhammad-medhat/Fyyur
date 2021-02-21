from app import *
#---------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# DONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
shows=db.Table('shows',    
    db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
    db.Column('start_date', db.DateTime)
)
# genres = db.Table('venuegenres', 
#                   db.col)
class Venue(db.Model):
    __tablename__ = 'Venue'

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String)
    city          = db.Column(db.String(120))
    state         = db.Column(db.String(120))
    address       = db.Column(db.String(120))
    phone         = db.Column(db.String(120))
    image_link    = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    # genres = db.Column('genres', db.String(50)) #Enum("Jazz", "Reggae", "Swing", "Classical", "Folk", "Rock n Roll"))
    artists = db.relationship('Artist', secondary=shows, backref=db.backref('Venue', lazy=True))
    def __repr__(self):
        return f"<Venue id:{self.id}, name:{self.name}>"

class Artist(db.Model):
    __tablename__ = 'Artist'

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String)
    city          = db.Column(db.String(120))
    state         = db.Column(db.String(120))
    phone         = db.Column(db.String(120))
    image_link    = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    # genres = db.Column( 'genres', db.String(50))#Enum("Jazz", "Reggae", "Swing", "Classical", "Folk", "Rock n Roll") )
    def __repr__(self):
        return f"<Artist id:{self.id}, name:{self.name}>"

import __data__