
import os
import speech_recognition as sr
from pydub import AudioSegment
import pydub
import tempfile
import logging
import shutil
from django.conf import settings

logger = logging.getLogger(__name__)

class AudioProcessor:
    """
    Class for processing audio files and converting them to text.
    """
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def convert_wav_to_text(self, audio_file_path):
        try:
            from urllib.parse import urlparse
            from django.conf import settings

            # Handle URL if provided
            if audio_file_path.startswith("http"):
                parsed = urlparse(audio_file_path)
                file_name = os.path.basename(parsed.path)
                audio_file_path = os.path.join(settings.MEDIA_ROOT, "audio_files", file_name)
                logger.info(f"Converted URL to local path: {audio_file_path}")

            # Check file existence and permissions
            logger.info(f"Processing file: {audio_file_path}")
            if not os.path.exists(audio_file_path):
                logger.error(f"File does not exist: {audio_file_path}")
                return {"success": False, "error": "File not found", "text": None}
            if not os.access(audio_file_path, os.R_OK):
                logger.error(f"No read permission for file: {audio_file_path}")
                return {"success": False, "error": "No read permission", "text": None}

            # Log file size
            logger.info(f"File size: {os.path.getsize(audio_file_path)} bytes")

            # Load audio
            try:
                audio = AudioSegment.from_wav(audio_file_path)
                logger.info(f"Audio details: duration={len(audio)/1000}s, sample_rate={audio.frame_rate}, channels={audio.channels}")
            except Exception as e:
                logger.error(f"Failed to load WAV file with pydub: {e}")
                return {"success": False, "error": f"Audio loading failed: {e}", "text": None}

            # Use a simple temporary file
            temp_path = os.path.join(tempfile.gettempdir(), "temp_audio.wav")
            logger.info(f"Exporting to temp file: {temp_path}")
            try:
                audio.export(temp_path, format="wav")
                if not os.path.exists(temp_path):
                    logger.error(f"Temporary file not created: {temp_path}")
                    return {"success": False, "error": "Failed to create temp file", "text": None}
                with sr.AudioFile(temp_path) as source:
                    audio_data = self.recognizer.record(source)
                    text = self.recognizer.recognize_google(audio_data, language="en-US")
                    return {"success": True, "error": None, "text": text}
            finally:
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                        logger.info(f"Removed temp file: {temp_path}")
                    except Exception as e:
                        logger.warning(f"Failed to remove temp file {temp_path}: {e}")

        except sr.UnknownValueError:
            logger.warning(f"Speech Recognition could not understand audio: {audio_file_path}")
            return {"success": False, "error": "Could not understand audio", "text": None}
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Speech Recognition service: {e}")
            return {"success": False, "error": f"API unavailable: {e}", "text": None}
        except Exception as e:
            logger.error(f"Error processing audio file {audio_file_path}: {e}")
            return {"success": False, "error": str(e), "text": None}