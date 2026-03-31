from app import app, db
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

#the User model: each user has a username, and a playlist_id foreign key referring
#to the user's Playlist  
class User(db.Model):
	id: Mapped[int] = mapped_column(primary_key = True)
	username: Mapped[str] = mapped_column(String(50),index = True, unique = True, nullable=False) 
	playlist_id: Mapped[int] = mapped_column(ForeignKey('playlist.id'), unique= True)

	# Relationship One - One
	playlist: Mapped["Playlist"] = relationship("Playlist", back_populates="user")
	
	#representation method
	def __repr__(self):
		return "{}".format(self.username)
	
	def serialize(self):
		return {
			"id": self.id,
			"username": self.username,
			"playlist_id": self.playlist_id
		}

#create the Song model here + add a nice representation method
class Song(db.Model):
	id: Mapped[int] = mapped_column(primary_key= True)
	artist: Mapped[str] = mapped_column(String(120), index = True, nullable = False)
	title: Mapped[str] = mapped_column(String(120), index = True, nullable = False)
	n: Mapped[int] = mapped_column(Integer)
		
	def __repr__(self):
		return f"{self.title} by {self.artist}"
	
	def serialize(self):
		return {
			"id": self.id,
			"artist": self.artist,
			"title": self.title
		}
	
#create the Item model here + add a nice representation method
class Item(db.Model):
	id: Mapped[int] = mapped_column(primary_key= True)
	song_id: Mapped[int] = mapped_column(ForeignKey('song.id'))
	playlist_id: Mapped[int] = mapped_column(ForeignKey('playlist.id'))

	# Relationship Many - One
	playlist: Mapped["Playlist"] = relationship("Playlist", back_populates="items")

	def __repr__(self):
		return f"Song id: {self.song_id} - Playlist id: {self.playlist_id}"
	
#create the Playlist model here + add a nice representation method
class Playlist(db.Model):
	id: Mapped[int] = mapped_column(primary_key= True)

	# Relationship One - One
	user: Mapped["User"] = relationship("User", back_populates="playlist", uselist=False)
	# Relationship One - Many
	items: Mapped[list["Item"]] = relationship("Item", back_populates="playlist", cascade="all, delete-orphan")

	def __repr__(self):
		return f"User: {self.user} - Playlist id: {self.id}"