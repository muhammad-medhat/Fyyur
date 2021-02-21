from app import db
from dbmodels import *

# from flask_sqlalchemy import get_debug_queries
# from SQLAlchemy import update
import json
import pprint
venuesList= [
    {
        "id": 1,
        "name": "The Musical Hop",
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "website": "https://www.themusicalhop.com",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    
    }, 
    {
        "id": 2,
        "name": "The Dueling Pianos Bar",
        "address": "335 Delancey Street",
        "city": "New York",
        "state": "NY",
        "phone": "914-003-1132",
        "facebook_link": "https://www.facebook.com/theduelingpianos",
        "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    "seeking_talent": False,
    "website": "https://www.theduelingpianos.com",
    "genres": ["Classical", "R&B", "Hip-Hop"],

    },
    {
        "id": 3,
        "name": "Park Square Live Music & Coffee",
        "address": "34 Whiskey Moore Ave",
        "city": "San Francisco",
        "state": "CA",
        "phone": "415-000-1234",
        "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
        "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "seeking_talent": False,    
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],    
    "website": "https://www.parksquarelivemusicandcoffee.com",



    }
]
artistsSimpleList = [
    {
        "id": 4,
        "name": "Guns N Petals",
    }, {
        "id": 5,
        "name": "Matt Quevedo",
    }, {
        "id": 6,
        "name": "The Wild Sax Band",
    }
]


artistsList=[
        {
            "id": 4,
            "name": "Guns N Petals",
            "genres": ["Rock n Roll"],
            "city": "San Francisco",
            "state": "CA",
            "phone": "326-123-5000",
            "website": "https://www.gunsnpetalsband.com",
            "facebook_link": "https://www.facebook.com/GunsNPetals",
            "seeking_venue": "True",
            "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
            "image_link": "https://images.unsplash.com/p-1549213783-8284d0336c4f?ixlib=rb-1.2.1&=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"   
        }, 
        {
                "id": 5,
                "name": "Matt Quevedo",
                "genres": ["Jazz"],
                "city": "New York",
                "state": "NY",
                "phone": "300-400-5000",
                "facebook_link": "https://www.facebook.com/mattquevedo923251523",
                "seeking_venue": "False",
                "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80"
        }, 
        {
                "id": 6,
                "name": "The Wild Sax Band",
                "genres": ["Jazz", "Classical"],
                "city": "San Francisco",
                "state": "CA",
                "phone": "432-325-5432",
                "seeking_venue": "False",
                "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80" 
        }
    ]


for v in venuesList:
    venue=Venue(id=v['id'], name=v['name'], city=v['city'], state=v['state'])
    db.session.add(venue)
db.session.commit()


# for a in artistsSimpleList:
#     art = Artist(id=a['id'], name = a['name'])
#     db.session.add(art)

# db.session.commit()
def key_exist(k, my_dict):
    return k in my_dict


# for a in artistsList:
#     artist = Artist.query.get(int(a['id']))

#     if key_exist('city'               , a) :  artist.city=                str(a['city'])                 
#     if key_exist('state'              , a) :  artist.state=               str(a['state'])                
#     if key_exist('phone'              , a) :  artist.phone=               str(a['phone'])                
#     if key_exist('website'            , a) :  artist.website=             str(a['website'])              
#     if key_exist('facebook_link'      , a) :  artist.facebook_link=       str(a['facebook_link'])        
#     if key_exist('seeking_venue'      , a) :  artist.seeking_venue=       str(a['seeking_venue'])        
#     if key_exist('seeking_description', a) :  artist.seeking_description= str(a['seeking_description'])  
#     if key_exist('image_link'         , a) :  artist.image_link=          str(a['image_link'])           
    
#     db.session.add(artist)

db.session.commit()


