# This files contains all the core functions that are then imported into app.py, the base Flask function.

# importing the openai package and the authentication key.
import openai
from key_computer3_oai import *
import re
import os

client = openai.OpenAI(api_key=key_api_key0)

# This functions creates a thread
def func_create_thread():

    run_id = client.beta.threads.create()
    
    return run_id.id


# This functions adds a user message to the thread.
def func_send_msg(user_input0, var_thread_id0):
    
    client.beta.threads.messages.create(

        thread_id=var_thread_id0,
        role="user",
        content=user_input0

    )


# This functions runs a thread.
def func_run_thread(form_county, var_thread_id0):

    run = client.beta.threads.runs.create_and_poll(

        thread_id=var_thread_id0,
        assistant_id=assistant_dict[form_county],

    )


# This retrieves the latest message after the thread is run
def func_retrieve_msg(var_thread_id0):
    messages = client.beta.threads.messages.list(
        
        thread_id=var_thread_id0

    )

    return messages.data[0].content[0].text.value


# This cleans the file.
def text_fix(text):

    # Replace double asterisks (**) with <strong> for bold text
    html_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Replace newline characters (\n) with <br> for line breaks
    html_text = html_text.replace('\n', '<br>')
    # Remove any text between 【 and 】
    html_text = re.sub(r'【.*?】', '', html_text)
    
    return html_text


# This runs the full cycle in one function.
def func_complete_cycle(subm_prompt, subm_county, var_thread_id0):
    
    func_send_msg(subm_prompt, var_thread_id0)
    func_run_thread(subm_county, var_thread_id0)
    
    function_output = text_fix(func_retrieve_msg(var_thread_id0))

    return function_output
