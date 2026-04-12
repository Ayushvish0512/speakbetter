from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
# Try to upload a tiny file and print state
with open('test.txt', 'w') as f:
    f.write('hello')

uploaded = client.files.upload(path='test.txt')
print(f"State: {uploaded.state}")
print(f"Dir: {dir(uploaded.state)}")
if hasattr(uploaded.state, 'name'):
    print(f"Name: {uploaded.state.name}")
