from api import app


def test_health_check():
    with app.test_client() as test_client:
        response = test_client.get("/ping")
        assert response.status_code == 200
        assert b"pong!" in response.data
