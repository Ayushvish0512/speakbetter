import google.generativeai as genai
from app.core.config import settings
import json

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash') # Using 1.5 flash as requested in PRD (corrected from 2.5)

    async def analyze_audio(self, audio_path: str):
        # Upload the file to Gemini
        audio_file = genai.upload_file(path=audio_path)
        
        prompt = """
        Analyze this audio recording of a person speaking English.
        Transcribe the audio and then provide correction and feedback.
        Return strictly valid JSON only:
        {
          "transcription": "What the user actually said",
          "corrected": "Corrected version of the sentence",
          "hindi": "Simple Hindi explanation of the correction",
          "feedback": "Encouraging comment",
          "score": 8
        }
        """
        
        response = self.model.generate_content([prompt, audio_file])
        try:
            text = response.text.strip()
            if text.startswith("```json"): text = text[7:-3].strip()
            elif text.startswith("```"): text = text[3:-3].strip()
            return json.loads(text)
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            return {
                "transcription": "Unknown",
                "corrected": "Unknown",
                "hindi": "क्षमा करें, मैं अभी इसका विश्लेषण नहीं कर सका।",
                "feedback": "Keep practicing!",
                "score": 5
            }

gemini_service = GeminiService()
