import os
import requests as http_requests
from flask import Flask, request, jsonify
from constants import *

app = Flask(__name__)

@app.route('/')
def root():
    return 'todoist service working'

@app.route('/update-task', methods=['POST'])
def update_todoist_task():
    data = request.get_json()
    id = data['id']
    task = data['task']
    todoist_task_url = str(TODOIST_BASE_API_URL) + 'tasks/' + str(id)
    headers = {"Authorization": "Bearer " + str(TODOIST_API_KEY)}
    http_requests.post(todoist_task_url, json=task, headers=headers)
    return 'OK'


# Fetch tasks from a todoist project
def get_todoist_project_tasks(TODOIST_FROGNET_PROJECT_ID):
    todoist_tasks_url = str(TODOIST_BASE_API_URL) + 'tasks/'
    headers = {"Authorization": "Bearer " + str(TODOIST_API_KEY)}
    r = http_requests.get(todoist_tasks_url, params={'project_id': TODOIST_FROGNET_PROJECT_ID}, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        return None

@app.route('/get-tasks', methods=['POST'])
def get_todos():
    tasks = get_todoist_project_tasks(TODOIST_FROGNET_PROJECT_ID)
    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT'))