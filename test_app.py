import pytest
from app import app, fibonacci

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_fibonacci_function():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(2) == 1
    assert fibonacci(3) == 2
    assert fibonacci(4) == 3
    assert fibonacci(5) == 5
    assert fibonacci(6) == 8
    assert fibonacci(10) == 55

def test_fibonacci_endpoint(client):
    # Test valid input
    response = client.get('/fibonacci?n=10')
    data = response.get_json()
    assert response.status_code == 200
    assert data['fibonacci'] == 55
    
    # Test missing parameter
    response = client.get('/fibonacci')
    assert response.status_code == 400
    
    # Test invalid parameter type
    response = client.get('/fibonacci?n=abc')
    assert response.status_code == 400
    
    # Test negative number
    response = client.get('/fibonacci?n=-1')
    assert response.status_code == 400

def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'healthy' 