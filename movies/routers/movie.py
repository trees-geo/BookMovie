from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from .. import schemas
from .. import models
from typing import List
from fastapi.params import Depends
from sqlalchemy.orm import Session
from ..database import get_database_session
from .login import get_current_user

router = APIRouter(tags=["Movie"], prefix= "/movie")

@router.post("/", status_code=201, response_model=schemas.MovieResponse)
def add_movie(movie: schemas.Movie, db: Session = Depends(get_database_session)):
    new_movie = models.Movie(name=movie.name, language=movie.language,
                             release_date=movie.release_date, ticket_price=movie.ticket_price, rating=movie.rating, producer_id=1)
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie

@router.get("/", response_model=List[schemas.MovieResponse])
def fetch_all_movies(db: Session = Depends(get_database_session), current_user:schemas.TokenUser = Depends(get_current_user)):
    movies = db.query(models.Movie).all()
    return movies

@router.get("/{id}", response_model=schemas.MovieResponse)
def fetch_movie(id: int, db: Session = Depends(get_database_session)):
    # print(type(id))
    movie = db.query(models.Movie).filter(models.Movie.id == id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie Not Found")
    return movie

@router.delete("/{id}")
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

@router.put("/{id}")
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