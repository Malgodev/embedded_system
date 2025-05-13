from django.db import models
from django.conf import settings
import os
import uuid

# Create your models here.
class AudioFile(models.Model):
    """Model for storing audio files and their transcription results"""
    
    # Unique identifier for each audio file
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Original filename of the uploaded file
    original_filename = models.CharField(max_length=255, blank=True)
    
    # The actual audio file
    audio_file = models.FileField(upload_to='audio_files/')
    
    # Text transcription of the audio
    transcription = models.TextField(blank=True, null=True)
    
    # Error message in case transcription fails
    error_message = models.TextField(blank=True, null=True)
    
    # Flag to indicate whether transcription was successful
    is_processed = models.BooleanField(default=False)
    is_successful = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.original_filename or self.id} - {'Processed' if self.is_processed else 'Pending'}"
    
    def get_file_path(self):
        """Get the absolute path to the audio file"""
        if self.audio_file:
            return os.path.join(settings.MEDIA_ROOT, self.audio_file.name)
        return None
    
    def save_transcription(self, transcription_result):
        """
        Save transcription results to the model
        
        Args:
            transcription_result (dict): Dictionary with keys 'success', 'error', 'text'
        """
        self.is_processed = True
        self.is_successful = transcription_result.get('success', False)
        
        if self.is_successful:
            self.transcription = transcription_result.get('text', '')
        else:
            self.error_message = transcription_result.get('error', 'Unknown error')
        
        self.save()

class AIHandler(models.Model):
    """Model for handle transcription and send back results with wav file"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    
    audio_file = models.FileField(upload_to='generated_audio/', null=True, blank=True)
    original_request = models.JSONField(null=True, blank=True)

    def get_audio_path(self):
        """Return the path to the generated audio file"""
        if self.audio_file:
            return self.audio_file.path
        return None

    def __str__(self):
        return f"TTS Request {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"