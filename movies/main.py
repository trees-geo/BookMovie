from fastapi import FastAPI
from .database import engine
from . import models
from .routers import producer, movie, login
from jose import jwt, JWTError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

SECRET_KEY = "602f625a03237d3c9d6baa7db0416a14de0dea17c56acfd78add111d6b6cfcc1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

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

# SKIP_AUTH_PATHS = ["/documentation", "/openapi.json", "/docs", "/redoc", "/login", "/public"]

# @app.middleware("http")
# async def verify_jwt_cookie(request: Request, call_next):
#     print(request)
#     # Skip auth for specific routes
#     if request.url.path in SKIP_AUTH_PATHS:
#         return await call_next(request)
    
#     token = request.headers.get("authorization")[7:] 

#     if not token:
#         return JSONResponse(status_code=401, content={"error": "Missing token"})

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True})
#         request.state.user = payload  # store decoded data for later use

#     except JWTError as e:
#         return JSONResponse(status_code=401, content={"error": f"{str(e)}"})

#     return await call_next(request)



app.include_router(movie.router)
app.include_router(producer.router)
app.include_router(login.router)
models.Base.metadata.create_all(engine)





