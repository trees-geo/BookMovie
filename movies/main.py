from fastapi import FastAPI
from .database import engine
from . import models
from .routers import producer, movie, login


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
app.include_router(movie.router)
app.include_router(producer.router)
app.include_router(login.router)
models.Base.metadata.create_all(engine)





