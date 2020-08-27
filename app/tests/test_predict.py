from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_valid_input():
    """Return 200 Success when input is valid."""
    response = client.post(
        '/predict',
        json={
            'title': 'First string',
            'body': 'Another string',
            'n': 1
        }
    )
    assert response.status_code == 200


def test_invalid_input():
    """Return 422 Validation Error when given non-strings"""
    response = client.post(
        '/predict',
        json={
            'title': -3.14,
            'body': 'this is a string',
            'n': 1
        }
    )
    response2 = client.post(
        '/predict',
        json={
            'title': 'a title',
            'body': 7,
            'n': 1
        }
    )
    response3 = client.post(
        '/predict',
        json={
            'title': 'title',
            'body': 'this is a string',
            'n': 'number'
        }
    )
    assert response.status_code == 422
    assert response2.status_code == 422
    assert response3.status_code == 422


if __name__ == "__main__":
    for func in (test_valid_input, test_invalid_input):
        func()
