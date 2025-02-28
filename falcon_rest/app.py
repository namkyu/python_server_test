from wsgiref import simple_server

import falcon

from resources import TodoListResource, TodoResource

app = falcon.App()
app.add_route('/todos', TodoListResource())  # 전체 목록 및 추가
app.add_route('/todos/{todo_id}', TodoResource())  # 개별 todo 조회, 수정, 삭제

if __name__ == '__main__':
    with simple_server.make_server('127.0.0.1', 8000, app) as server:
        print("Falcon API 서버 실행 중 : http://127.0.0.1:8000")
        server.serve_forever()
