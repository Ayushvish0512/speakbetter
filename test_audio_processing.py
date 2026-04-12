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
model = genai.GenerativeModel('gemini-1.5-flash')

audio_path = r"C:\Users\Admin\Downloads\9773796763_7005737079_20251120_171342.mp3"

def test_audio():
    if not os.path.exists(audio_path):
        print(f"Error: File not found at {audio_path}")
        return

    print(f"Uploading {audio_path}...")
    audio_file = genai.upload_file(path=audio_path)
    
    prompt = """
    Analyze this audio recording of a person speaking English.
    Transcribe the audio and then provide correction and feedback for a Hindi-speaking beginner.
    Return strictly valid JSON only:
    {
      "transcription": "...",
      "corrected": "...",
      "hindi": "...",
      "feedback": "...",
      "score": 0-10
    }
    """
    
    print("Generating content...")
    response = model.generate_content([prompt, audio_file])
    print(response.text)

if __name__ == "__main__":
    test_audio()
