import os

OPEN_AI_API_KEY = os.environ.get('OPEN_AI_API_KEY')
SYSTEM_PROMPT = 'You are an AI language model trained to analyze and detect the priority of todo tasks.'
USER_PROMPT = 'Analyze the following array of tasks and score the task from 1 to 4 while 4 is highest and 1 is lowest. Return only the score in a list:'