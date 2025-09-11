from typing import Optional
from pydantic import BaseModel
from datetime import date

class Movie(BaseModel):
    id: int
    name: str
    language: str
    release_date: date
    ticket_price: float
    rating: str

class ProducerResponse(BaseModel):
    name: str
    email: str

    model_config = {
        "from_attributes":True
    }
class MovieResponse(BaseModel):
    id: int
    name: str
    language: str
    release_date: date
    rating: str
    producer: ProducerResponse

    model_config = {
        "from_attributes": True
    }  

class Producer(BaseModel):
    name: str
    email: str
    password: str

class User(BaseModel):
    user: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenUser(BaseModel):
    username: Optional[str] = None
    refresh_token: Optional[str] = None