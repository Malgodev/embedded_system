from django.db import models

# Create your models here.
class AudioTranscription(models.Model):
    audio_file = models.FileField(upload_to='audio_uploads/')
    text_result = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transcription {self.id} - {self.created_at}"