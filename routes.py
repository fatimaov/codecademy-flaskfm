from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from app import app, db
from models import User, Song, Playlist, Item
from flask import render_template, request, url_for, redirect, flash
from sqlalchemy import select

#A form for inputing new songs via Dashboard
class SongForm(FlaskForm):
  title = StringField(label = "Song Title:", validators=[DataRequired()])
  artist = StringField(label = "Artist:", validators=[DataRequired()])
  submit = SubmitField("Add Song")

#A function we made to check if an item to be added is already in the playlist
def exists(item, playlist):
  """Return a boolean
    True if playlist contains item. False otherwise.
    """
  for i in playlist: #for each item in playlist
    if i.song_id == item.song_id: #check if the primary key is equal
       return True
  return False

#The home page of FlaskFM
#Lists all the users currently in the database
#renders the home.html template providing the list of current users
@app.route('/profiles')
def profiles():
    current_users = db.session.execute(select(User)).scalars().all() #change here to a database query
    return render_template('users.html', current_users = current_users)

#Displays profile pages for a user with the user_id primary key
#renders the profile.html template for a specific user, song library and 
#the user's playlist 
@app.route('/profile/<int:user_id>')
def profile(user_id):
   user = db.get_or_404(User, user_id, description = "No such user found.")
   songs = db.session.execute(select(Song)).scalars().all()
   my_playlist = db.session.get(Playlist, user.playlist_id) #change here to a database query
   return render_template('profile.html', user = user, songs = songs, my_playlist = my_playlist)

#Adds new songs to a user's playlist from the song library
#redirects back to the profile that issued the addition
@app.route('/add_item/<int:user_id>/<int:song_id>/<int:playlist_id>')
def add_item(user_id, song_id, playlist_id):
   new_item = Item(song_id = song_id, playlist_id = playlist_id)
   user = db.get_or_404(User, user_id, description = "No such user found.")
   my_playlist = db.session.execute(select(Playlist).where(Playlist.id == user.playlist_id)).scalars().first()
   if not exists(new_item, my_playlist.items):
      song = db.session.get(Song, song_id)
      #using db session add the new item
      db.session.add(new_item)
      #increase the counter for the song associated with the new item
      song.n += 1
      #commit the database changes here
      db.session.commit()
   return redirect(url_for('profile', user_id = user_id))

#Remove an item from a user's playlist
#Redirects back to the profile that issues the removal
@app.route('/remove_item/<int:user_id>/<int:item_id>')
def remove_item(user_id, item_id):
   #from the Item model, fetch the item with primary key item_id to be deleted
   item = db.session.get(Item, item_id)
   #using db.session delete the item
   db.session.delete(item)
   #commit the deletion
   db.session.commit()
   return redirect(url_for('profile', user_id = user_id))
   
#Display the Dashboard page with a form for adding songs
#Renders the dashboard template
@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
  form = SongForm()
  if request.method == 'POST' and form.validate():
    #create a new song here
    new_song = Song(title = form.title.data, artist = form.artist.data, n = 1)
    #add it to the database
    db.session.add(new_song)
    #commit to the database
    db.session.commit()
    # Redirect after POST
    return redirect(url_for('dashboard'))
  else:
        flash(form.errors)
  unpopular_songs = db.session.execute(select(Song).order_by(Song.n)).scalars().all()  #add the ordering query here
  songs = db.session.execute(select(Song)).scalars().all()
  return render_template('dashboard.html', songs = songs, unpopular_songs = unpopular_songs, form = form)