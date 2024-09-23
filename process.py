import openai
from key_computer3_oai import *

client = openai.OpenAI(api_key=key_api_key0)


def func_run_thread(var_instructions0=''):
    run = client.beta.threads.runs.create_and_poll(
    thread_id=var_thread_id0,
    assistant_id=assistant_id0,
    instructions=var_instructions0
    )

    return run

def func_send_msg(user_input0):
    client.beta.threads.messages.create(
    thread_id=var_thread_id0,
    role="user",
    content=user_input0
    )


def func_retrieve_msg():
    messages = client.beta.threads.messages.list(
        thread_id=var_thread_id0
    )

    return messages.data[0].content[0].text.value

def func_complete_cycle(user_input0):
    func_send_msg(user_input0)
    func_run_thread()
    function_output = func_retrieve_msg()

    return function_output