import speech_recognition as sr
import shutil

flac_path = shutil.which("flac")
if flac_path:
    sr.audio.FLAC_CONVERTER = flac_path
else:
    raise EnvironmentError("FLAC converter not found — ensure 'flac' is installed and in PATH.")