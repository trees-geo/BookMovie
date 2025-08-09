from .database import Base
from sqlalchemy import Column, String, Date, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Movie(Base):
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    language = Column(String)
    release_date = Column(Date)
    ticket_price = Column(Float)
    rating = Column(String)
    producer_id = Column(Integer, ForeignKey("producer.id"))
    producer = relationship("Producer", back_populates="movie")

class Producer(Base):
    __tablename__ = "producer"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    movie = relationship("Movie", back_populates="producer")
