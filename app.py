from flask import Flask, render_template, request, redirect, url_for
from key_computer3_oai import *
from db_package import *
from datetime import datetime

app = Flask(__name__)


#Base home page.
@app.route('/')
def home():
    return render_template('index.html')

global_thread = "threads/thread_wqrYgWSOoth0ZYf3YeIov9Jx"
global_county = "Sonoma"



#When the route is /submit, it posts the information. It takes, input_user and category
@app.route('/submit', methods=['POST', 'GET'])
def submit():
    global global_thread, global_county

    # Handle GET requests by redirecting to home
    if request.method == 'GET':
        return redirect(url_for('home'))

    #creates a thread
    var_thread_id0=(client.beta.threads.create()).id
    global_thread = var_thread_id0
    
    print(var_thread_id0)


    #puts in prompts
    subm_prompt = request.form.get('form_prompt')
    if subm_prompt is None or subm_prompt.strip() == "":
        subm_prompt = "What is the fine for littering?"
    
    subm_email = request.form.get('form_email')
    if subm_email is None or subm_email.strip() == "":
        subm_email = "null"

    subm_county=request.form.get('form_county')
    global_county = subm_county

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    output_0=f'{timestamp} - Thread: {global_thread} | - Question: {subm_prompt} | County: {global_county}\n'
    with open('log.txt', 'a') as f:
        f.write(output_0)
    
    # Calls the thread, then writes the reponse.
    response_prompt = func_complete_cycle(subm_prompt, global_county, global_thread)    
    response_0=f'{timestamp} - Thread: {global_thread} | - Response: {repr(response_prompt)} | County: {global_county}\n'
    with open('log.txt', 'a') as f:
        f.write(response_0)   
    
    return render_template('conversation.html', response_prompt=response_prompt, response_county=subm_county)





#When the route is /conversation, on the followup
@app.route('/conversation', methods=['POST', 'GET'])
def conversation():
    global global_thread, global_county

    # Handle GET requests by redirecting to home
    if request.method == 'GET':
        return redirect(url_for('home'))

    subm_prompt = request.form.get('form_prompt')
    if subm_prompt is None or subm_prompt.strip() == "":
        subm_prompt = "followup"

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    output_0=f'{timestamp} - Thread: {global_thread} |  - Question: {subm_prompt} | County: {global_county}\n'

    with open('log.txt', 'a') as f:
        f.write(output_0)


    response_prompt = func_complete_cycle(subm_prompt, global_county, global_thread)    
    response_0=f'{timestamp} - Thread: {global_thread} | Question: {repr(response_prompt)} | County: {global_county}\n'
    with open('log.txt', 'a') as f:
        f.write(response_0)   

    return render_template('conversation.html', response_prompt=response_prompt, response_county=global_county)



if __name__ == '__main__':
    # Run the Flask app on all available IP addresses
    app.run(host='0.0.0.0', port=5000, debug=True)

