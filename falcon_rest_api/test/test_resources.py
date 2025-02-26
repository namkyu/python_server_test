import json

import falcon
import pytest
from falcon import testing

from falcon_rest_api.resources import TodoListResource, TodoResource


# 테스트 케이스 실행될 때마다 새로운 데이터 초기화
@pytest.fixture
def client():
    app = falcon.App()
    app.add_route('/todos', TodoListResource())
    app.add_route('/todos/{todo_id}', TodoResource())
    return testing.TestClient(app)


def test_get_todos(client):
    response = client.simulate_get('/todos')
    assert response.status == falcon.HTTP_200
    data = json.loads(response.text)
    assert isinstance(data, list)
    assert len(data) > 0


def test_create_todo(client):
    new_todo = {"title": "Falcon 테스트", "done": False}
    response = client.simulate_post('/todos', json=new_todo)
    assert response.status == falcon.HTTP_201
    data = json.loads(response.text)
    assert data["title"] == new_todo["title"]
    assert "id" in data


def test_get_specific_todo(client):
    response = client.simulate_get('/todos/1')
    assert response.status == falcon.HTTP_200
    data = json.loads(response.text)
    assert data["id"] == 1


def test_update_todo(client):
    update_data = {"title": "update title", "done": True}
    response = client.simulate_put('/todos/1', json=update_data)
    assert response.status == falcon.HTTP_200
    data = json.loads(response.text)
    assert data["title"] == "update title"
    assert data["done"] is True


def test_delete_todo(client):
    response = client.simulate_delete('/todos/1')
    assert response.status == falcon.HTTP_200
    response = client.simulate_get('/todos/1')
    assert response.status == falcon.HTTP_404
