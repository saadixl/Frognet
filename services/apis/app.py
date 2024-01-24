import ast
import os
from flask import Flask, request, jsonify
import requests as http_requests

app = Flask(__name__)

@app.route('/')
def root():
    return 'api service working'

# Endpoint for sorting todo list
@app.route('/sort-todo-list', methods=['POST'])
def sort_todo_list():
    todoist_url = 'http://todoist:5702/get-todos'
    todoist_response = http_requests.post(todoist_url)
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
        todo_list_with_score = []
        i = 0
        if scores is not None:
            for t in todo_list:
                todo_list_with_score.append({
                    'item': todoist_tasks[i],
                    'score': scores[i]
                })
                i = i + 1

        # Sort the todo list
        sorted_todo_list = sorted(todo_list_with_score, key=lambda x: x['score'], reverse=True)

    return jsonify({
        'sorted_todo_list': sorted_todo_list,
        'scores': scores
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT'))