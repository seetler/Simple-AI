from openai import OpenAI
from openai_key import *

client = OpenAI(
api_key=key
)

input_vers=input('Vers: --->|')
input_user=input('User: --->|')
input_syst=input('Syst: --->|')

model_dict={'35':'gpt-3.5-turbo', '40':'gpt-4o'}

model_vers=model_dict[input_vers]
# --df


completion = client.chat.completions.create(
  model=model_vers,
  messages=[
    {"role": "system", "content": input_syst},
    {"role": "user", "content": input_user}
  ]
)

print(completion.choices[0].message.content)