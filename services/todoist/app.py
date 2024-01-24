import os
import requests as http_requests
from flask import Flask, request, jsonify

app = Flask(__name__)
TODOIST_API_KEY = os.environ.get('TODOIST_API_KEY')
TODOIST_FROGNET_PROJECT_ID = os.environ.get('TODOIST_FROGNET_PROJECT_ID')
TODOIST_BASE_API_URL = 'https://api.todoist.com/rest/v2/'

@app.route('/')
def root():
    return 'todoist service working'

# Fetch tasks from a todoist project
def get_todoist_project_tasks(TODOIST_FROGNET_PROJECT_ID):
    todoist_tasks_url = str(TODOIST_BASE_API_URL) + 'tasks/'
    headers = {"Authorization": "Bearer " + str(TODOIST_API_KEY)}
    r = http_requests.get(todoist_tasks_url, params={'project_id': TODOIST_FROGNET_PROJECT_ID}, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        return None

@app.route('/get-todos', methods=['POST'])
def get_todos():
    tasks = get_todoist_project_tasks(TODOIST_FROGNET_PROJECT_ID)
    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT'))