import ast
import os
from flask import Flask, request, jsonify
import requests as http_requests

app = Flask(__name__)

@app.route('/')
def root():
    return 'api service working'


@app.route('/reset-tasks', methods=['POST'])
def reset_tasks():
    todoist_get_task_url = 'http://todoist:5702/get-tasks'
    todoist_response = http_requests.post(todoist_get_task_url)
    todoist_tasks = todoist_response.json().get('tasks')

    if todoist_tasks is not None:
        for task in todoist_tasks:
            id = task.get('id')
            todoist_update_url = 'http://todoist:5702/update-task'
            task.update({
                'priority': int(1)
            })
            http_requests.post(todoist_update_url, json = {
                'id': id,
                'task': task
            })
    return 'OK'

# Endpoint for sorting todo list
@app.route('/sort-todo-list', methods=['POST'])
def sort_todo_list():
    todoist_get_task_url = 'http://todoist:5702/get-tasks'
    todoist_response = http_requests.post(todoist_get_task_url)
    todoist_tasks = todoist_response.json().get('tasks')

    if todoist_tasks is not None:
        todo_list = []
        for task in todoist_tasks:
            todo_list.append(task.get('content'))

        # Calling the openai service to score the todo list texts
        url = 'http://openai:5700/score-texts'
        json_payload = {'texts': todo_list}
        r = http_requests.post(url=url, json=json_payload)

        # Sending response
        if r.status_code == 200:
            try:
                r_json = r.json()
                scores_str = r_json.get('scores')
                # Convert a string like '[1, 2, 3]' into a list
                scores = ast.literal_eval(scores_str)
            except:
                scores = None
        else:
            scores = None

        # Insert score with the todo list
        updated_sorted_list = []
        if scores is not None:
            i = 0
            for task in todoist_tasks:
                id = task.get('id')
                todoist_update_url = 'http://todoist:5702/update-task'
                task.update({
                    'priority': int(scores[i])
                })
                updated_sorted_list.append(task)
                http_requests.post(todoist_update_url, json = {
                    'id': id,
                    'task': task
                })
                i = i + 1

    return jsonify({
        'updated_sorted_list': updated_sorted_list,
        'scores': scores
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT'))