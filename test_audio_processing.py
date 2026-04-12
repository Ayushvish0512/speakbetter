import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv(dotenv_path="backend/.env")

# Try to get the key from env or .env
api_key = os.getenv("GEMINI_API_KEY")
if not api_key or api_key == "your_gemini_api_key_here":
    print("Error: GEMINI_API_KEY not found in environment or .env file.")
    # I'll check if the user provided it in a way I can extract
    # For now, I'll exit
    exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash-preview-tts')

audio_path = r"C:\Users\Admin\Downloads\9773796763_7005737079_20251120_171342.mp3"

def test_audio():
    print(f"Uploading {audio_path}...")
    audio_file = genai.upload_file(path=audio_path)
    
    prompt = """
    You are a supportive English coach. 
    1. Listen to the user's audio.
    2. Provide a correction and encouragement.
    3. Return a JSON object with:
       {
         "transcription": "...",
         "corrected": "...",
         "hindi": "...",
         "feedback": "...",
         "score": 1-10
       }
    4. Also generate a natural SPOKEN response to be returned as audio.
    """
    
    print("Generating Native Speech content...")
    response = model.generate_content(
        [prompt, audio_file],
        generation_config={"response_modalities": ["text", "audio"]}
    )
    
    # Save text response
    with open("result.json", "w", encoding="utf-8") as f:
        f.write(response.candidates[0].content.parts[0].text)
    
    # Save audio response if present
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'inline_data'):
            with open("response_audio.wav", "wb") as f:
                f.write(part.inline_data.data)
            print("Native AI Speech saved to response_audio.wav")
            
    print("Text result saved to result.json")

if __name__ == "__main__":
    test_audio()
