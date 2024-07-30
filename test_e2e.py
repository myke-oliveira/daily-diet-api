import requests

BASEURL = "http://localhost:5000"

# Não deve ser possivel cadastrar um novo usuário sem username
def test_create_user_without_username():
    url = f"{BASEURL}/user"
    payload = {}
    response = requests.post(url, json=payload)
    assert response.status_code == 400
    assert response.json().get("message") == "Invalid credentials"
    
def test_create_user():
    url = f"{BASEURL}/user"
    payload = {
        "username": "username",
        "password": "password"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 201
    
    response_data = response.json()
    assert response_data.get("message") == "User created"
    assert response_data.get("user").get("username") == payload.get("username")
    assert type(response_data.get("user").get("id")) == int