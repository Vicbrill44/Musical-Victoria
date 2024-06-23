from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, DateTime,Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime

# Database setup
DATABASE_URL = "sqlite:////home/victorvas/data/musical-victoria.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# SQLAlchemy models
class Artist(Base):
    __tablename__ = 'artist'
    artist_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    artist_name = Column(String, nullable=False)
    artist_crtd_dt = Column(DateTime, default=datetime.utcnow)
    artist_updt_dt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Song(Base):
    __tablename__ = 'song'
    song_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    song_name = Column(String, nullable=False)
    song_artist_id = Column(Integer, ForeignKey('artist.artist_id'), nullable=False)
    song_crtd_dt = Column(DateTime, default=datetime.utcnow)
    song_updt_dt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    artist = relationship("Artist", back_populates="songs")

class Meaning(Base):
    __tablename__ = 'meaning'
    meaning_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    meaning_song_id = Column(Integer, ForeignKey('song.song_id'), nullable=False)
    meaning_generated = Column(Text, nullable=False)
    meaning_crtd_dt = Column(DateTime, default=datetime.utcnow)
    meaning_updt_dt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    song = relationship("Song", back_populates="meanings")

class FeedbackMeaning(Base):
    __tablename__ = 'feedback_meaning'
    feedback_meaning_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    feedback_meaning_meaning_id = Column(Integer, ForeignKey('meaning.meaning_id'), nullable=False)
    feedback_meaning_rating = Column(Integer, nullable=False)
    feedback_meaning_crtd_dt = Column(DateTime, default=datetime.utcnow)
    feedback_meaning_updt_dt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    meaning = relationship("Meaning", back_populates="feedbacks")

# Establish relationships
Artist.songs = relationship("Song", back_populates="artist")
Song.meanings = relationship("Meaning", back_populates="song")
Meaning.feedbacks = relationship("FeedbackMeaning", back_populates="meaning")

# Pydantic models for data transfer objects
class ArtistBase(BaseModel):
    artist_name: str

class ArtistCreate(ArtistBase):
    pass

class ArtistRead(ArtistBase):
    artist_id:int

    class Config:
        orm_mode = True

#-----------------------------

class SongBase(BaseModel):
    song_name: str
    song_artist_id:int

class SongCreate(SongBase):
    pass

class SongRead(SongBase):
    song_id:int

    class Config:
        orm_mode = True

#-----------------------------

class MeaningBase(BaseModel):
    meaning_generated: str
    meaning_song_id:int


class MeaningCreate(MeaningBase):
    pass

class MeaningRead(MeaningBase):
    meaning_id:int

    class Config:
        orm_mode = True

#-----------------------------

class FeedbackMeaningBase(BaseModel):
    feedback_meaning_rating: int
    feedback_meaning_meaning_id:int


class FeedbackMeaningCreate(FeedbackMeaningBase):
    pass

class FeedbackMeaningRead(FeedbackMeaningBase):
    feedback_meaning_id:int

    class Config:
        orm_mode = True

app = FastAPI()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/artist/", response_model=ArtistRead)
def create_artist(artist: ArtistCreate, db: Session = Depends(get_db)):
    db_artist = Artist(
        artist_name=artist.artist_name
    )
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist


@app.get("/artist/{artist_id}", response_model=ArtistRead)
def get_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = db.query(Artist).filter(Artist.artist_id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist

#----------

@app.post("/song/", response_model=SongRead)
def create_song(song: SongCreate, db: Session = Depends(get_db)):
    db_song = Song(
        song_name=song.song_name,
        song_artist_id=song.song_artist_id
    )
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song

@app.get("/song/{song_id}", response_model=SongRead)
def get_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.song_id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

#--------
@app.post("/meaning/", response_model=MeaningRead)
def create_meaning(meaning: MeaningCreate, db: Session = Depends(get_db)):
    db_meaning = Meaning(
        meaning_song_id=meaning.meaning_song_id,
        meaning_generated=meaning.meaning_generated
    )
    db.add(db_meaning)
    db.commit()
    db.refresh(db_meaning)
    return db_meaning

@app.get("/meaning/{meaning_id}", response_model=MeaningRead)
def get_meaning(meaning_id: int, db: Session = Depends(get_db)):
    meaning = db.query(Meaning).filter(Meaning.meaning_id == meaning_id).first()
    if not meaning:
        raise HTTPException(status_code=404, detail="Meaning not found")
    return meaning

#--------
@app.post("/feedback_meaning/", response_model=FeedbackMeaningRead)
def create_feedback_meaning(feedback_meaning: FeedbackMeaningCreate, db: Session = Depends(get_db)):
    db_feedback_meaning = FeedbackMeaning(
        feedback_meaning_rating=feedback_meaning.feedback_meaning_rating,
        feedback_meaning_meaning_id=feedback_meaning.feedback_meaning_meaning_id
    )
    db.add(db_feedback_meaning)
    db.commit()
    db.refresh(db_feedback_meaning)
    return db_feedback_meaning

@app.get("/feedback_meaning/{feedback_meaning_id}", response_model=FeedbackMeaningRead)
def get_feedback_meaning(feedback_meaning_id: int, db: Session = Depends(get_db)):
    feedback_meaning = db.query(FeedbackMeaning).filter(FeedbackMeaning.feedback_meaning_id == feedback_meaning_id).first()
    if not feedback_meaning:
        raise HTTPException(status_code=404, detail="Feedback Meaning not found")
    return feedback_meaning


# Create database tables
Base.metadata.create_all(bind=engine)
