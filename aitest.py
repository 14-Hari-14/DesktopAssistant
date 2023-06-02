import os
import openai
from config import apikey

openai.api_key = apikey

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="write an email for leave \n",
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response)

'''
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "text": "\nSubject: Request for Leave\n\nDear [Employer],\n\nI am writing to inform you that I need to take a leave of absence from work. The leave of absence will start [date] and end [date].\n\nThe reason I am taking leave is [state reason]. This will give me enough time to [state reason].\n\nI understand that taking a leave of absence might cause some disruption to the team, and I am willing to do whatever I can to ensure that my work is done before I leave. I am happy to answer any questions and provide additional information. \n\nI look forward to hearing from you.\n\nSincerely,\n[Your Name]"
    }
  ],
  "created": 1684600327,
  "id": "cmpl-7IJmxvxLvQZUAk891Bn2hdb1NHPL2",
  "model": "text-davinci-003",
  "object": "text_completion",
  "usage": {
    "completion_tokens": 142,
    "prompt_tokens": 7,
    "total_tokens": 149
  }
}
'''