import os
from flask import Flask, jsonify
from constants import todoist_get_task_url
from helpers import call_other_service, get_scores_from_openai, update_task

app = Flask(__name__)

@app.route('/')
def root():
    return 'api service working'

# Endpoint for reseting task priorities
@app.route('/reset-tasks', methods=['POST'])
def reset_tasks():
    todoist_tasks = call_other_service(todoist_get_task_url).json().get('tasks')
    if todoist_tasks is not None:
        for task in todoist_tasks:
            id = task.get('id')
            task.update({
                'priority': int(1)
            })
            update_task(id, task)
    return 'OK'



# Endpoint for sorting todo list
@app.route('/auto-prioritize-tasks', methods=['POST'])
def auto_prioritize_tasks():
    todoist_tasks = call_other_service(todoist_get_task_url).json().get('tasks')
    if todoist_tasks is not None:
        task_contents = []
        for task in todoist_tasks:
            task_contents.append(task.get('content'))

        scores = get_scores_from_openai(task_contents)

        # Use score as the priority
        if scores is not None:
            i = 0
            for task in todoist_tasks:
                id = task.get('id')
                task.update({'priority': int(scores[i])})
                update_task(id, task)
                i = i + 1

    return jsonify({
        'scores': scores
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT'))