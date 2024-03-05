from flask import Flask, request, jsonify
from flask_cors import CORS
import os, logging
from collections import deque
from groq import Groq

app = Flask(__name__)
CORS(app, origins=["*.groq.com", "*.googleapis.com"])
logging.basicConfig(level=logging.DEBUG)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
user_messages = deque(maxlen=100)
bot_responses = deque(maxlen=100)

def query_groq_api(user_message):
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": user_message,
        }],
        model="mixtral-8x7b-32768",
    )
    response_content = chat_completion.choices[0].message.content
    user_messages.append(user_message)
    bot_responses.append(response_content)
    return response_content

@app.route('/chat', methods=['POST'])
def handle_chat():
    try:
        request_data = request.json
        user_message = request_data['message']['text']
        groq_response = query_groq_api(user_message)
        google_chat_response = {
            "text": groq_response
        }
        return jsonify(google_chat_response)
    except Exception as e:
        return jsonify({"text": f"Error handling the request: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)