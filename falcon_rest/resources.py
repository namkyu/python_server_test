import json

import falcon

todos = [
    {"id": 1, "title": "Python 학습", "done": False},
    {"id": 2, "title": "Falcon API 만들어 보기", "done": False},
    {"id": 3, "title": "Fast API 만들어 보기", "done": False}
]


def json_response(resp, data, status=falcon.HTTP_200):
    resp.status = status
    resp.content_type = 'application/json'
    resp.text = json.dumps(data, ensure_ascii=False)


class TodoListResource:

    def on_get(self, req, res):
        json_response(res, todos)

    def on_post(self, req, res):
        try:
            raw_json = req.bounded_stream.read()
            todo_data = json.loads(raw_json)

            new_todo = {
                "id": todos[-1]["id"] + 1 if todos else 1,
                "title": todo_data["title"],
                "done": todo_data.get("done", False)
            }
            todos.append(new_todo)
            json_response(res, new_todo, falcon.HTTP_201)
        except Exception as e:
            json_response(res, {"error": str(e)}, falcon.HTTP_400)


class TodoResource:

    def on_get(self, req, res, todo_id):
        todo = next((t for t in todos if t["id"] == int(todo_id)), None)
        if todo:
            json_response(res, todo)
        else:
            json_response(res, {"error": "TODO not found"}, falcon.HTTP_404)

    def on_put(self, req, res, todo_id):
        todo = next((t for t in todos if t["id"] == int(todo_id)), None)
        if not todo:
            json_response(res, {"error": "TODO not found"}, falcon.HTTP_404)
            return

        raw_json = req.bounded_stream.read()
        todo_data = json.loads(raw_json)

        todo["title"] = todo_data.get("title", todo["title"])
        todo["done"] = todo_data.get("done", todo["done"])

        json_response(res, todo)

    def on_delete(self, req, res, todo_id):
        global todos
        todos = [t for t in todos if t["id"] != int(todo_id)]
        json_response(res, {"message": "TODO deleted"}, falcon.HTTP_200)
