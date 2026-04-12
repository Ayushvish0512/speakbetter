from google import genai
from google.genai import types
import os
import json
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
response = client.models.generate_content(
    model='gemini-2.0-flash', # use a stable one
    contents='Respond in JSON: {"hello": "world"}',
    config=types.GenerateContentConfig(
        response_mime_type='application/json'
    )
)
print(f"Response Text: {response.text}")
try:
    data = json.loads(response.text)
    print(f"Parsed: {data}")
except Exception as e:
    print(f"Failed to parse: {e}")
