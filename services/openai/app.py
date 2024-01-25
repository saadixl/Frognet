import os
import openai
from flask import Flask, request, jsonify
from constants import *

app = Flask(__name__)
openai.api_key = OPEN_AI_API_KEY

@app.route('/')
def root():
    return 'openai service working'


@app.route('/score-texts', methods=['POST'])
def score_texts():
    data = request.get_json()
    texts = data['texts']
    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': f'{USER_PROMPT} {texts}'}
    ]

    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        max_tokens=20,
        n=1,
        stop=None,
        temperature=0
    )
    scores = completion.choices[0].message.content

    return jsonify({'scores': scores})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT'))