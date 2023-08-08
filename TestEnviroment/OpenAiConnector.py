import json
import os

import openai as gpt
import requests
from dotenv import load_dotenv

load_dotenv()

gpt.api_key = os.getenv("OPENAI_API_KEY")
ask_question = "Test API "

target_url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {gpt.api_key}",
    "Content-Type": "application/json"
}
request_data = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": f"{ask_question}\n"}],
    "temperature": 0.5,
}
new_session = requests.session()

response = new_session.post(target_url, data=json.dumps(request_data), headers=headers)

print(response.json())
