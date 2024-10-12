from flask import Flask, render_template, request
from key_computer3_oai import *
from db_package import *

app = Flask(__name__)

#Base home page.
@app.route('/')
def home():
    return render_template('index.html')

global_thread = None
global_county = None

#When the route is /submit, it posts the information. It takes, input_user and category
@app.route('/submit', methods=['POST'])
def submit():

    global global_thread, global_county

    #creates a thread
    var_thread_id0=(client.beta.threads.create()).id
    global_thread = var_thread_id0
    print(var_thread_id0)


    #puts in prompts
    subm_prompt = request.form.get('form_prompt')
    subm_county=request.form.get('form_county')
    global_county = subm_county
    print(assistant_dict[subm_county])

    response_prompt = func_complete_cycle(subm_prompt, subm_county, var_thread_id0)
    print(repr(response_prompt))
    return render_template('conversation.html', response_prompt=response_prompt, response_county=subm_county)





#When the route is /submit, on the followup
@app.route('/conversation', methods=['POST'])
def conversation():

    global global_thread, global_county


    #puts in prompts
    subm_prompt = request.form.get('form_prompt')
    subm_county=global_county
    print(assistant_dict[subm_county])

    response_prompt = func_complete_cycle(subm_prompt, subm_county, global_thread)
    print(repr(response_prompt))
    return render_template('conversation.html', response_prompt=response_prompt, response_county=subm_county)





#Base home page.
@app.route('/greet')
def greet():
    return render_template('greet.html')


if __name__ == '__main__':
    # Run the Flask app on all available IP addresses
    app.run(host='0.0.0.0', port=5000, debug=True)

