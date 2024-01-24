import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)
OPEN_AI_API_KEY = os.environ.get("OPEN_AI_API_KEY")
openai.api_key = OPEN_AI_API_KEY

@app.route('/')
def welcome():
    return 'openai service working'

@app.route('/score-texts', methods=['POST'])
def sentiment_analysis():
    data = request.get_json()
    texts = data['texts']
    messages = [
        {"role": "system", "content": "You are an AI language model trained to analyze and detect the priority of todo tasks."},
        {"role": "user", "content": f"Analyze the following array of tasks and score the task from 1 to 10. Return only the score in a list: {texts}"}
    ]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=20,
        n=1,
        stop=None,
        temperature=0
    )
    response_text = completion.choices[0].message.content

    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT'))