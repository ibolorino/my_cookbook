
def test_health(client):
    response = client.get('/health')

    expected = {
        'status': 'running',
        'version': 'v1'
    }

    assert response.status_code == 200
    assert response.json() == expected
