import pandas as pd
from pydantic import BaseModel
from openai import OpenAI
import os
import json


# load data
data = pd.read_excel("data/raw/atmospere_data.xlsx")
print(data['working_atmosphere_comment'][0])


class StepByStepAIResponse(BaseModel):
    topic: str
    short_sumary: str
    one_word_summary: str
    positve: bool
    

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)

prompt = f"""I am performing an sentiment analyse. Please Evaluate the following statement from a job portal in kontext 
a feel-good atmosphere:
{data['working_atmosphere_comment'][0]}

return  a list of the general topic, a short summary, a one word summary and a boolean if the statement is positve or not.
[topic, short_sumary, one_word_summary, positve]
"""

completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
)

output = json.loads(completion.choices[0]["message"])
print(output)
