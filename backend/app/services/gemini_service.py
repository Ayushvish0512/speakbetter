from google import genai
from google.genai import types
from app.core.config import settings
import json
import base64
import io
import wave
import asyncio

class GeminiService:
    def __init__(self):
        # Using the new Google GenAI SDK
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        # Models
        self.analysis_model = "gemini-2.5-flash"
        self.tts_model = "gemini-2.5-flash-preview-tts"

    async def analyze_audio(self, audio_path: str):
        try:
            print(f"DEBUG: Starting analyze_audio for {audio_path}")
            # 1. Upload audio file to Gemini
            # Corrected argument: 'file' instead of 'path'
            audio_file = self.client.files.upload(
                file=audio_path, 
                config=types.UploadFileConfig(mime_type='audio/webm')
            )
            print(f"DEBUG: Uploaded file {audio_file.name}, state={audio_file.state}")

            # Wait for file to become active
            import time
            start_time = time.time()
            while audio_file.state.name == "PROCESSING":
                if time.time() - start_time > 30:
                    raise Exception("File processing timed out")
                await asyncio.sleep(1)
                audio_file = self.client.files.get(name=audio_file.name)
            
            if audio_file.state.name == "FAILED":
                raise Exception(f"Audio processing failed: {audio_file.error}")
            
            print(f"DEBUG: File is ACTIVE. Uri: {audio_file.uri}")

            # 2. Stage One: Multimodal Analysis
            analysis_prompt = """
            Analyze this student's English speaking audio.
            Return a JSON object with EXACTLY these keys:
            {
              "transcription": "What they said",
              "corrected": "The perfect natural English version",
              "hindi": "A short explanation in Hindi of the correction",
              "feedback": "A very short encouraging sentence for the student",
              "score": 1-10
            }
            """
            
            analysis_response = self.client.models.generate_content(
                model=self.analysis_model,
                contents=[
                    types.Content(
                        parts=[
                            types.Part(text=analysis_prompt),
                            types.Part(file_data=types.FileData(file_uri=audio_file.uri, mime_type=audio_file.mime_type))
                        ]
                    )
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1 # Low temperature for consistent JSON
                )
            )
            
            if not analysis_response.text:
                raise Exception("Empty response from analysis model")

            print(f"DEBUG: Analysis response: {analysis_response.text[:100]}...")
            
            # Robust JSON parsing
            try:
                # Remove any markdown junk if present
                raw_json = analysis_response.text
                if "```json" in raw_json:
                    raw_json = raw_json.split("```json")[1].split("```")[0].strip()
                elif "```" in raw_json:
                    raw_json = raw_json.split("```")[1].split("```")[0].strip()
                analysis_data = json.loads(raw_json)
            except Exception as jse:
                print(f"DEBUG: JSON parse error: {jse}. Raw: {analysis_response.text}")
                # Try simple find if regex fails
                import re
                match = re.search(r'\{.*\}', analysis_response.text, re.DOTALL)
                if match:
                    analysis_data = json.loads(match.group())
                else:
                    raise jse

            # 3. Stage Two: High-Quality Native TTS Response
            tts_prompt = f"""
            # AUDIO PROFILE: Kore
            ## THE SCENE: A supportive English tutoring session.
            ### DIRECTOR'S NOTES: Supportive, clear, and encouraging vocal smile.
            #### TRANSCRIPT:
            {analysis_data['feedback']} Your corrected sentence is: {analysis_data['corrected']}
            """

            audio_base64 = None
            try:
                # Adding a small retry for intermittent 500 errors from preview models
                for attempt in range(2):
                    try:
                        tts_response = self.client.models.generate_content(
                            model=self.tts_model,
                            contents=tts_prompt,
                            config=types.GenerateContentConfig(
                                response_modalities=["AUDIO"],
                                speech_config=types.SpeechConfig(
                                    voice_config=types.VoiceConfig(
                                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                            voice_name='Kore'
                                        )
                                    )
                                )
                            )
                        )
                        
                        if tts_response.candidates and tts_response.candidates[0].content.parts:
                            part = tts_response.candidates[0].content.parts[0]
                            if part.inline_data:
                                pcm_data = part.inline_data.data
                                print(f"DEBUG: Generated TTS audio of size {len(pcm_data)}")
                                
                                # Convert raw PCM to WAV
                                with io.BytesIO() as wav_io:
                                    with wave.open(wav_io, 'wb') as wf:
                                        wf.setnchannels(1)
                                        wf.setsampwidth(2)
                                        wf.setframerate(24000)
                                        wf.writeframes(pcm_data)
                                    wav_bytes = wav_io.getvalue()
                                
                                audio_base64 = base64.b64encode(wav_bytes).decode('utf-8')
                        break # Success
                    except Exception as e:
                        if attempt == 0:
                            print(f"DEBUG: TTS Attempt 1 failed, retrying... Error: {e}")
                            await asyncio.sleep(1)
                        else:
                            raise e

            except Exception as tts_e:
                print(f"DEBUG: Stage 2 (TTS) failed entirely: {tts_e}. Falling back to browser TTS.")
                # We don't raise here, we just continue with audio_base64 as None

            analysis_data['audio_data'] = audio_base64
            print(f"DEBUG: Analysis processed (TTS Success: {audio_base64 is not None})")
            return analysis_data

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Gemini GenAI Error:\n{error_details}")
            return {
                "transcription": "Error processing audio",
                "corrected": "Technical error occurred",
                "hindi": "त्रुटि। कृपया बाद में प्रयास करें।",
                "feedback": f"Details: {str(e)[:100]}",
                "score": 0,
                "audio_data": None
            }

gemini_service = GeminiService()
