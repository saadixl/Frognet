import os

TODOIST_GET_TASK_URL = 'http://todoist:5702/get-tasks'
TODOIST_UPDATE_TASK_URL = 'http://todoist:5702/update-task'
OPENAI_SCORE_TEXT_URL = 'http://openai:5700/score-texts'
AUTO_PRIORITIZE_ENDPOINT = os.environ.get('AUTO_PRIORITIZE_ENDPOINT')