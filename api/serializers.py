from rest_framework import serializers
from .models import AudioFile, AIHandler
from .speech_generator import SpeechProcessor

class AudioFileSerializer(serializers.ModelSerializer):
    """Serializer for the AudioFile model"""
    
    class Meta:
        model = AudioFile
        fields = [
            'id', 'original_filename', 'audio_file', 
            'transcription', 'error_message', 
            'is_processed', 'is_successful',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'transcription', 'error_message', 
            'is_processed', 'is_successful',
            'created_at', 'updated_at'
        ]

class AudioTranscriptionResultSerializer(serializers.ModelSerializer):
    """Serializer for transcription results"""
    
    class Meta:
        model = AudioFile
        fields = [
            'id', 'original_filename', 
            'transcription', 'error_message', 
            'is_processed', 'is_successful',
            'created_at', 'updated_at'
        ]
        read_only_fields = fields

class AIProcessSerializer(serializers.Serializer):
    response_id = serializers.UUIDField()
    request_text = serializers.CharField()
    response_text = serializers.CharField()
    audio_link = serializers.URLField(allow_null=True)
    is_successful = serializers.BooleanField()
    created_at = serializers.DateTimeField()
