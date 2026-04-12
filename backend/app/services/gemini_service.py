import google.generativeai as genai
from app.core.config import settings
import json

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('models/gemini-3-flash-preview')

    async def analyze_audio(self, audio_path: str):
        # Upload the file to Gemini
        audio_file = genai.upload_file(path=audio_path)
        
        # System instructions to return both JSON data and Spoken Feedback
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
        
        # Requesting both text (for JSON) and audio (for native speech)
        try:
            response = self.model.generate_content(
                [prompt, audio_file],
                generation_config={"response_modalities": ["TEXT", "AUDIO"]}
            )
        except Exception as e:
            print(f"Gemini Native Audio Error: {e}. Falling back to Text-only.")
            # Fallback to standard model
            fallback_model = genai.GenerativeModel('models/gemini-1.5-flash')
            response = fallback_model.generate_content([prompt, audio_file])
        
        try:
            # Extract JSON data and Audio data
            text_part = ""
            audio_base64 = None
            
            for part in response.candidates[0].content.parts:
                # Check for text (many ways text can be returned)
                if hasattr(part, 'text') and part.text:
                    text_part += part.text
                # Check for native speech audio data
                if hasattr(part, 'inline_data') and part.inline_data:
                    import base64
                    audio_base64 = base64.b64encode(part.inline_data.data).decode('utf-8')

            if text_part.startswith("```json"): text_part = text_part[7:-3].strip()
            elif text_part.startswith("```"): text_part = text_part[3:-3].strip()
            
            result = json.loads(text_part)
            if audio_base64:
                result["audio_data"] = audio_base64 # Attach native speech
            
            return result
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            return {
                "transcription": "Unknown",
                "corrected": "Unknown",
                "hindi": "क्षमा करें, तकनीकी त्रुटि।",
                "feedback": "Keep practicing!",
                "score": 5
            }

gemini_service = GeminiService()
