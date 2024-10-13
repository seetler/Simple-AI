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
        subm_prompt = "Can I camp in parks? Are there fees?"
    
    subm_email = request.form.get('form_email')
    if subm_email is None or subm_email.strip() == "":
        subm_email = "null"

    subm_county=request.form.get('form_county')



    global_county = subm_county
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')



    with open('log.txt', 'a') as f:
        f.write(f'{timestamp} - Email: {subm_email} \n')
    
    with open('log.txt', 'a') as f:
        f.write(f'{timestamp} - Thread: {global_thread} |  - Question: {subm_prompt} | County: {subm_county}\n')
    
    print(assistant_dict[subm_county])
    print(subm_prompt)

    response_prompt = func_complete_cycle(subm_prompt, subm_county, var_thread_id0)
    
    with open('log.txt', 'a') as f:
        f.write(f'{timestamp} - Thread: {global_thread} | Question: {repr(response_prompt)} | County: {subm_county}\n')   
    
    print(repr(response_prompt))
    return render_template('conversation.html', response_prompt=response_prompt, response_county=subm_county)





#When the route is /submit, on the followup
@app.route('/conversation', methods=['POST'])
def conversation():

    global global_thread, global_county



    subm_prompt = request.form.get('form_prompt')
    if subm_prompt is None or subm_prompt.strip() == "":
        subm_prompt = "followup"


  #puts in prompts

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open('log.txt', 'a') as f:
        f.write(f'{timestamp} - Thread: {global_thread} |  - Question: {subm_prompt} | County: {global_county}\n')
    
    print(assistant_dict[global_county])
    print(subm_prompt)

    response_prompt = func_complete_cycle(subm_prompt, global_county, global_thread)
    
    with open('log.txt', 'a') as f:
        f.write(f'{timestamp} - Thread: {global_thread} | Question: {repr(response_prompt)} | County: {global_county}\n')   
    
    print(repr(response_prompt))
    return render_template('conversation.html', response_prompt=response_prompt, response_county=global_county)




#Base home page.
@app.route('/greet')
def greet():
    return render_template('greet.html')


if __name__ == '__main__':
    # Run the Flask app on all available IP addresses
    app.run(host='0.0.0.0', port=5000, debug=True)

