from app import app, db
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

#the User model: each user has a username, and a playlist_id foreign key referring
#to the user's Playlist  
class User(db.Model):
  id: Mapped[int] = mapped_column(primary_key = True)
  username: Mapped[str] = mapped_column(String(50),index = True, unique = True, nullable=False) 
  playlist_id: Mapped[int] = mapped_column(ForeignKey('playlist.id'))
  
  #representation method
  def __repr__(self):
        return "{}".format(self.username)
  
  def serialize(self):
        return {
            "id": self.id,
            "username": self.username
        }

#create the Song model here + add a nice representation method
    
#create the Item model here + add a nice representation method
    
#create the Playlist model here + add a nice representation method
