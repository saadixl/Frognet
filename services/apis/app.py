import ast
import os
from flask import Flask, request, jsonify
import requests as http_requests
from constants import todoist_get_task_url, todoist_update_url, openai_score_text_url

app = Flask(__name__)

@app.route('/')
def root():
    return 'api service working'

# Method for calling todoist service
def call_todoist_service(url, json={}):
    todoist_response = http_requests.post(url, json = json)
    return todoist_response

# Method for calling openai service
def call_openai_service(url, json={}):
    openai_response = http_requests.post(url, json = json)
    return openai_response

# Endpoint for reseting task priorities
@app.route('/reset-tasks', methods=['POST'])
def reset_tasks():
    todoist_tasks = call_todoist_service(todoist_get_task_url).json().get('tasks')

    if todoist_tasks is not None:
        for task in todoist_tasks:
            id = task.get('id')
            task.update({
                'priority': int(1)
            })
            call_todoist_service(todoist_update_url, {
                'id': id,
                'task': task
            })
    return 'OK'

# Endpoint for sorting todo list
@app.route('/auto-prioritize-tasks', methods=['POST'])
def auto_prioritize_tasks():
    todoist_tasks = call_todoist_service(todoist_get_task_url).json().get('tasks')

    if todoist_tasks is not None:
        task_contents = []
        for task in todoist_tasks:
            task_contents.append(task.get('content'))

        # Calling the openai service to score the todo list texts
        openai_response = call_openai_service(openai_score_text_url, {'texts': task_contents})

        # Sending response
        if openai_response.status_code == 200:
            try:
                scores_str = openai_response.json().get('scores')
                # Convert a string like '[1, 2, 3]' into a list
                scores = ast.literal_eval(scores_str)
            except:
                scores = None
        else:
            scores = None

        # Insert score with the todo list
        if scores is not None:
            i = 0
            for task in todoist_tasks:
                id = task.get('id')
                task.update({'priority': int(scores[i])})
                call_todoist_service(todoist_update_url, {
                    'id': id,
                    'task': task
                })
                i = i + 1

    return jsonify({
        'scores': scores
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT'))