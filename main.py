from fastapi import FastAPI, Form, status
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime, date, time, timedelta
from uuid import UUID, uuid4
from typing import List, Set
from fastapi.responses import Response

class Profile(BaseModel):
    name: str
    email: str
    age: int
    created_on: date
    created_at: time
    event_id: UUID

    class Config:
        json_schema_extra = {
            "example": {
                "name": "tree",
                "email": "trees",
                "age": 24,
                "created_on": datetime.now().date(), # string also works
                "created_at": datetime.now().time(),
                "event_id": uuid4() # or default_factory=uuid4 if using field example
            }
        }

class Image(BaseModel):
    name: str
    url: HttpUrl

class Product(BaseModel):
    id: int
    name: str
    price: float = Field(title="Price of item", gt=0, description="cost")
    discount: float
    discounted_price: float
    tags : set[str] = set() # this works, even [] because Pydantic automatically coerces the input to match the field type.
    # tags : List[str] = []
    # image: Image
    image: list[Image] # Nested model

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "IPad",
                "price": 1000,
                "discount": 5.5,
                "discounted_price": 0,
                "tags": ["ipad", "ipad mini", "apple ipad"],
                "image": [
                    {"name": "apple ipad",
                     "url": "https://www.google.com/"
                    },
                    {"name": "samsung ipad",
                     "url": "https://www.google.com/"
                    }
                ]
            }
        }

class Offers(BaseModel):
    name: str
    description: str
    price: float
    products: list[Product] # Deeply Nested model

class User(BaseModel):
    name: str = Field(example="ricky")
    nick_name: list[str] = Field(example=["rick", "morty"]) # no need to make strings, give it as is
    email: str = Field(example="ricky@morty")
    age: int = Field(example=33)

app = FastAPI()

@app.get("/")
def index():
    return "Hey"

@app.get("/property")
def property():
    return "MY property"

@app.get("/movies")
def movies():
    return {"Tarzan": "ANimation", "Spiderman": "Comics"}

@app.get("/property/{id}")
def dynamic(id: int):
    return f"This is dynamic path parameter {id}"

@app.get("/user/{username}")
def profile(username:str):
    return f"THis is {username}'s profile page"

@app.get("/product", status_code=status.HTTP_200_OK)
def products(id:int = 0, type:str = "electronics"):
    return f"THe product id is {id} and type of the product is {type}"

@app.get("/user/{username}/comments", status_code=status.HTTP_200_OK)
def profile(username:str, commentid:int):
    return f"THis is the {username}'s associated comment id : {commentid}"

@app.post("/adduser", status_code=status.HTTP_201_CREATED)
def add(profile: Profile):
    name = profile.name
    return f"User: {name} added successfully"

@app.post("/addproduct", status_code=status.HTTP_201_CREATED)
def addproduct(product:Product):
    product.discounted_price = product.price - (product.price * product.discount / 100)
    return product

@app.post("/addproduct/{product_id}")
def addproduct(product: Product, product_id: int, category: str):
    product.discounted_price = product.price - (product.price * product.discount / 100)
    return {"ID": product_id, "Product": product, "Category": category}

@app.post("/purchase")
def purchase(product: Product, user: User):
    return {"User": user, "Product": product}

@app.post("/offers")
def offers(offers:Offers):
    return offers

@app.post("/login")
def login(username:str = Form(...), password:str = Form(...)):
    return f"Hi {username}"