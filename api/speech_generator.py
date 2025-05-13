import os
from django.conf import settings
import uuid
import gtts
import google.generativeai as genai

genai.configure(api_key=settings.GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-lite")

base_promt = " in 50 words or less. Format the answer for text-to-speech: Avoid symbols, and use natural language that sounds good when spoken."

class SpeechProcessor:
    """Class for processing text and handling text-to-speech conversion"""
    
    def __init__(self):
        self.output_dir = os.path.join(settings.MEDIA_ROOT, 'generated_audio')
        # Create the directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

    def process_text(self, text):
        prompt = text + base_promt
        
        ai_response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3, 
                max_output_tokens=100
            )
        )

        return ai_response.text
    
    def generate_speech(self, text, language='en'):
        """Convert text to speech and save as a WAV file"""
        try:
            # Generate a unique filename
            filename = f"{uuid.uuid4()}.wav"
            output_path = os.path.join(self.output_dir, filename)
            
            # Use gTTS to convert text to speech
            tts = gtts.gTTS(text=text, lang=language)
            
            # Save the audio file
            tts.save(output_path)
            
            # Return the relative path from MEDIA_ROOT
            return os.path.join('generated_audio', filename)
        
        except Exception as e:
            print(f"Error generating speech: {str(e)}")
            return None
        
    def process_and_convert(self, ai_handler, language='en'):
        """Process text from AIHandler instance and convert to speech"""
        try:
            request_text = ai_handler.text_content
            
            response_text = self.process_text(request_text)
            
            audio_path = self.generate_speech(response_text, language)
            
            if audio_path:
                ai_handler.audio_file = audio_path
                ai_handler.processed = True
                ai_handler.save()
                
                return {
                    'success': True,
                    'audio_path': audio_path,
                    'request_text': request_text,
                    'response_text': response_text
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to generate audio file'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }