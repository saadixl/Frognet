import ast
import requests as http_requests
from constants import todoist_get_task_url, todoist_update_url, openai_score_text_url

# Method for calling other services
def call_other_service(url, json={}):
    response = http_requests.post(url, json = json)
    return response

# Method for updating todoist tasks
def update_task(id, task):
    call_other_service(todoist_update_url, {
        'id': id,
        'task': task
    })

# Method for getting scores from openai
def get_scores_from_openai(texts):
    # Calling the openai service to score the todo list texts
    openai_response = call_other_service(openai_score_text_url, {'texts': texts})

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
    return scores