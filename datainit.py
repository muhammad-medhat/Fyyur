
from app import db, Venue, Artist
from flask_sqlalchemy import get_debug_queries
# from SQLAlchemy import update
import json
import pprint

venuesList= [
    {
    "id": 1,
    "name": "The Musical Hop",
    "city": "San Francisco",
    "state": "CA",        
    "address":'',
    "phone":'',
    "image_link":'',
    "facebook_link":''
    }, 
    {
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "city": "New York",
    "state": "NY",
    "phone":'',
    "image_link":'',
    "facebook_link":'',
    "state": "CA",        
    "address":'',
    "phone":'',
    "image_link":'',
    "facebook_link":''
    },
    {
        "id": 3,
        "name": "Park Square Live Music & Coffee",
        "num_upcoming_shows": 1,
        "city": "San Francisco",
        "state": "CA",
        "address":'',
        "phone":'',
        "image_link":'',
        "facebook_link":''
    }
]
artistsList = [
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
artistsListUpdated='''
{
    "arts":[
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

}
'''
showslist = [
    {
        "artist_id":4, 
        "past_shows": [{
            "venue_id": 1,
            "venue_name": "The Musical Hop",
            "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
            "start_time": "2019-05-21T21:30:00.000Z"
            }]
            }, {
                "artist_id":5, 
                "past_shows": [{
                "venue_id": 3,
                "venue_name": "Park Square Live Music & Coffee",
                "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
                "start_time": "2019-06-15T23:00:00.000Z"
                }],
            }, {
                "artist_id":6, 
                    "upcoming_shows": [{
                    "venue_id": 3,
                    "venue_name": "Park Square Live Music & Coffee",
                    "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
                    "start_time": "2035-04-01T20:00:00.000Z"
                    }, {
                    "venue_id": 3,
                    "venue_name": "Park Square Live Music & Coffee",
                    "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
                    "start_time": "2035-04-08T20:00:00.000Z"
                    }, {
                    "venue_id": 3,
                    "venue_name": "Park Square Live Music & Coffee",
                    "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
                    "start_time": "2035-04-15T20:00:00.000Z"
                    }]
            }
]

# for v in venuesList:
#     venue=Venue(id=v['id'], name=v['name'], city=v['city'], state=v['state'])
#     db.session.add(venue)
artJson=json.loads(artistsListUpdated)

for (k, v) in artJson.items():
    # art=json.loads(v)
    
    for aList in v:
        # print(aList['id'])
        artist = Artist.query.get(aList['id'])
        for (artK, artV) in aList.items():
            # print(f"{artK}: {artV}")    
            # print(f"================")
    # 
    
            artist.genres=   'sssssssssss'
            artist.city = 'sssssssssss'
            artist.state=  'sssssssssss'
            artist.phone=  'sssssssssss'
            artist.website=  'sssssssssss'
            artist.facebook_link=  'sssssssssss'
            artist.seeking_venue=  'sssssssssss'
            artist.seeking_description=  'sssssssssss'
            artist.image_link='sssssssssss'
            # artist.genres= aList['genres']
            # artist.city= aList['city']
            # artist.state= aList['state']
            # artist.phone= aList['phone']
            # artist.website= aList['website']
            # artist.facebook_link= aList['facebook_link']
            # artist.seeking_venue= aList['seeking_venue']
            # artist.seeking_description= aList['seeking_description']
            # artist.image_link= aList['image_link']
            
            # db.session.add(artist)
            # print(aList['website'])
            # info = get_debug_queries()
            # pprint(info )
    
db.session.commit()



    # stmt = (
    #     update(user_table).
    #     where(user_table.c.id == 5).
    #     values(name='user #5')
    # )    
    # db.session.add(artist)

# artsList = json.loads(artistsListUpdated)
# print(artsList)
# for art in artsList['artistsList'] :
#     # print(artistsListUpdated)
#     print(art)
    # print(type(art))
###########################print(artistsListUpdated)
# print(json.JSONEncoder().encode(artistsListUpdated))
f='''
{

"popup": {
    "menuitem": [
    {"value": "New", "onclick": "CreateNewDoc()"},
    {"value": "Open", "onclick": "OpenDoc()"},
    {"value": "Close", "onclick": "CloseDoc()"}
    ]
}
}
'''
# data=json.loads(artistsListUpdated)
# # data=json.loads(f)
# for (k, v) in data.items():
#     print("Key: " + k)
#     print("Value: " + str(v))   



