# This files contains all the core functions that are then imported into app.py, the base Flask function.
# Currently for simplicity sakes, all are using the same thread and Assistant ID, however in the future this needs to be distinguished.

# importing the openai package and the authentication key.
import openai
from key_computer3_oai import *

client = openai.OpenAI(api_key=key_api_key0)



# This functions adds a user message to a thread.
def func_send_msg(user_input0):
    client.beta.threads.messages.create(
    thread_id=var_thread_id0,
    role="user",
    content=user_input0
    )

# This functions runs a thread. The purpose of having this function is to have a way to insert variables into the OpenAI client.beta.threads.runs.create_and_poll function.
def func_run_thread(var_instructions0=''):
    # this is setup where this is the function, however the outer shell allows insertion of thread ID, assistant ID, and instructions.
    run = client.beta.threads.runs.create_and_poll(
    thread_id=var_thread_id0,
    assistant_id=assistant_id0,
    instructions=var_instructions0
    )

    return run

# This retries the latest message after the thread is run
def func_retrieve_msg():
    messages = client.beta.threads.messages.list(
        thread_id=var_thread_id0
    )

    return messages.data[0].content[0].text.value

# This runs the full cycle in one function.
def func_complete_cycle(user_input0):
    func_send_msg(user_input0)
    func_run_thread()
    function_output = func_retrieve_msg()

    return function_output