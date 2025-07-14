from flask import json
from app import app

def test_get_house_price(client):
    response = client.get('/api/price?bedrooms=3&bathrooms=2&area=1500')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'price' in data

def test_get_house_price_invalid_params(client):
    response = client.get('/api/price?bedrooms=three&bathrooms=two&area=fifteen-hundred')
    assert response.status_code == 400

def test_post_house_price(client):
    response = client.post('/api/price', json={
        'bedrooms': 3,
        'bathrooms': 2,
        'area': 1500
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'price' in data

def test_post_house_price_invalid_data(client):
    response = client.post('/api/price', json={
        'bedrooms': 'three',
        'bathrooms': 'two',
        'area': 'fifteen-hundred'
    })
    assert response.status_code == 400