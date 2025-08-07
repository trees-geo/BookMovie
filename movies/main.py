from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from . import schemas
from .database import engine, Base, session
from . import models
from typing import List
from fastapi.params import Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(
    title="BookMyMovie API",
    description="Book tickets effortlessly with our seamless API endpoints",
    terms_of_service="http://www.linkedin.com/in/treesaangelgeorge",
    contact={
        "Developer Name": "Treesa George",
        "email": "treesa@yahoo.com",
        "website": "http://www.linkedin.com/in/treesaangelgeorge"
    },
    license_info={
        "name": "Treesa",
        "url": "http://www.linkedin.com/in/treesaangelgeorge"
    },
    docs_url="/documentation"
)

models.Base.metadata.create_all(engine)
# Base.metadata.create_all(engine)

def get_database_session():
    db = session()
    try:
        yield db
    finally:
        db.close()

@app.post("/movie", status_code=201, response_model=schemas.MovieResponse, tags=["Movie"])
def add_movie(movie: schemas.Movie, db: Session = Depends(get_database_session)):
    new_movie = models.Movie(name=movie.name, language=movie.language,
                             release_date=movie.release_date, ticket_price=movie.ticket_price, rating=movie.rating, producer_id=1)
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie

@app.get("/movies", response_model=List[schemas.MovieResponse], tags=["Movie"])
def fetch_all_movies(db: Session = Depends(get_database_session)):
    movies = db.query(models.Movie).all()
    return movies

@app.get("/movie/{id}", response_model=schemas.MovieResponse, tags=["Movie"])
def fetch_movie(id: int, db: Session = Depends(get_database_session)):
    # print(type(id))
    movie = db.query(models.Movie).filter(models.Movie.id == id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie Not Found")
    return movie

@app.delete("/movie/{id}", tags=["Movie"])
def delete_movie(id: int, db: Session = Depends(get_database_session)):
    movie = db.query(models.Movie).filter(models.Movie.id == id).first()
    print(type(movie))
    if not movie:
        raise HTTPException(status_code=404, detail="Movie Not Found")
    # db.delete(movie, synchronize_session=False)  
    db.delete(movie)  
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Movie deleted successfully"
    )

@app.put("/movie/{id}", tags=["Movie"])
def update_movie(id:int, request: schemas.Movie, db: Session = Depends(get_database_session)):
    movie = db.query(models.Movie).filter(models.Movie.id == id)
    if not movie.first():
        raise HTTPException(status_code=404, detail="Movie Not Found")
    movie.update(request.model_dump())
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Movie details updated successfully"
    )

@app.post("/addproducer", response_model=schemas.ProducerResponse, tags=['Producer'])
def add_producer(request: schemas.Producer, db: Session = Depends(get_database_session)):
    hashed_pwd = pwd_context.hash(request.password)
    new_producer = models.Producer(name=request.name, email=request.email, password=hashed_pwd)
    db.add(new_producer)
    db.commit()
    db.refresh(new_producer)
    return JSONResponse(
        status_code=201,
        content="Producer added successfully"
    )