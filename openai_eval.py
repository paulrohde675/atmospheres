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

completion = client.completions.create(
    model="gpt-3.5-turbo",
    prompt=[
       {"role": "user", "content": data['working_atmosphere_comment'][0]}
    ],
    functions=[
        {
          "name": "summarize_job_portal_rating",
          "description": "Summarize the job portal rating with a general topic, a short summary, a one word summary and a positive or negative sentiment",
          "parameters": StepByStepAIResponse.schema()
        }
    ],
    function_call={"name": "summarize_job_portal_rating"}
)

output = json.loads(completion.choices[0]["message"]["function_call"]["arguments"])
print(output)
