from flask import Flask, Response, request, jsonify, send_from_directory, render_template
from key_computer3_oai import *
from db_package import *
from datetime import datetime
import openai
import time

OPENAI_API_KEY =key_api_key0
ASSISTANT_ID = assistant_dict["Sonoma"]


app = Flask(__name__)


# ✅ Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

@app.route('/')
def home():
    """Serve the frontend HTML"""
    return render_template("index.html")

def stream_openai_response(prompt):
    """Generator function to interact with OpenAI Assistant API with new threads."""
    
    # 1️⃣ Create a new thread for every request
    thread = client.beta.threads.create()
    thread_id = thread.id  # Unique for each request

    # 2️⃣ Add the user's message to the new thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )

    # 3️⃣ Run the assistant on the new thread
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID
    )

    # 4️⃣ Wait for the assistant to process the request
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status == "completed":
            break
        time.sleep(1)  # Wait before checking again

    # 5️⃣ Retrieve the assistant's response and stream it to the frontend
    messages = client.beta.threads.messages.list(thread_id=thread_id)

    for msg in messages.data:
        if msg.role == "assistant":
            formatted_text = text_fix(msg.content)  # ✅ Apply text cleanup
            yield formatted_text.encode("utf-8")  # ✅ Convert string to bytes

    # **🔹 Add this line to send an "END_RESPONSE" marker to the frontend**
    yield b"\nEND_RESPONSE"


@app.route('/chat', methods=['POST'])
def chat():
    """Handles chat requests and streams OpenAI Assistant's response"""
    data = request.json
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    return Response(stream_openai_response(prompt), content_type='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=5000)