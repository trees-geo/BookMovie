from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_movies():
    api_response = client.get("/movies")
    assert api_response.json() == {"Tarzan": "ANimation", "Spiderman": "Comics"}
    assert api_response.status_code == 200

def test_profile():
    api_response = client.get("/user/ricky/comments?commentid=5")
    assert api_response.json() == "THis is the ricky's associated comment id : 5"
    assert api_response.status_code == 200

def test_addproduct():
    product = {"id": 5, "name": "Starlink Standard Kit", "price": 250, "discount": 5, 
               "image": [{"name": "starlink1", "url": "https://share.google/5Cl1qa0ev5lKQy0cH"}]}
    product["discounted_price"] = product["price"] - (product["price"] * product["discount"] / 100)
    api_response = client.post("/addproduct/5?category=Electronics", json=product)
    api_discounted_price = api_response.json()["Product"]["discounted_price"]
    expected_discounted_price = float(product["price"] - (product["price"] * product["discount"] / 100))
    assert api_discounted_price == expected_discounted_price
    assert api_response.status_code == 200
    