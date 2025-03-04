from flask import Flask, Response, request, jsonify, send_from_directory, render_template
from keys_hidden import *
from db_package import *
from datetime import datetime
import openai
import time

# This sets up a set of default keys.
# Because this version only uses a single assistant, we just Sonoma.
# The dictionary comes from keys_hidden.py
OPENAI_API_KEY =key_api_key0


# Sets root folder, and sets this file as the main.
app = Flask(__name__)


#  Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Visiting Base App Route causes home() to immediately trigger serving the index.html.
@app.route('/')
def home():
    # Serves the index.html
    return render_template("index.html")

# The /chat is triggered when the Submit button is pressed. It calls a function stream_openai_response from db_packages.py
@app.route('/chat', methods=['POST'])
def chat():
    # Some HTML moving.
    data = request.json
    prompt = data.get("prompt", "").strip()  # Trim whitespace to avoid false positives

    # Default Statement
    if not prompt:
        prompt = "Where can I get help with senior housing assistance?"

    return Response(stream_openai_response(prompt), content_type='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=5000)