import os
import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AudioFile, AIHandler
from .serializers import AudioFileSerializer, AudioTranscriptionResultSerializer, AIProcessSerializer
from .audio_processor import AudioProcessor
from .speech_generator import SpeechProcessor
import uuid
from django.conf import settings

# Create your views here.
class AudioFileViewSet(viewsets.ModelViewSet):
    """ViewSet for handling audio file uploads and transcription"""
    
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer
    
    def get_serializer_class(self):
        if self.action == 'retrieve' and self.request.method == 'GET':
            return AudioTranscriptionResultSerializer
        return AudioFileSerializer
    
    def perform_create(self, serializer):
        """Handle file upload and start transcription process"""
        audio_file = self.request.FILES.get('audio_file')
        original_filename = audio_file.name if audio_file else None
        
        # Save the AudioFile instance
        instance = serializer.save(original_filename=original_filename)
        
        # Initialize the audio processor
        processor = AudioProcessor()
        
        # Get the file path
        file_path = instance.get_file_path()
        
        # Process the audio file
        if file_path and os.path.exists(file_path):
            result = processor.convert_wav_to_text(file_path)
            instance.save_transcription(result)

class AIProcessViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        try:
            # Validate UUID
            uuid_obj = uuid.UUID(pk)

            # Fetch JSON from /api/audio/<uuid>/
            audio_api_url = f"http://127.0.0.1:8000/api/audio/{pk}/"
            response = requests.get(audio_api_url)

            if response.status_code != 200:
                return Response({
                    'error': 'Failed to fetch transcription data'
                }, status=status.HTTP_400_BAD_REQUEST)

            data = response.json()
            transcription = data.get('transcription')
            is_successful = data.get('is_successful')
            created_at = data.get('created_at')
            error_message = data.get('error_message')

            # Check if transcription is successful and available
            if not is_successful or transcription is None:
                return Response({
                    'error': 'Transcription failed or unavailable',
                    'error_message': error_message or 'No transcription provided',
                    'response_id': str(uuid_obj),
                    'created_at': created_at
                }, status=status.HTTP_400_BAD_REQUEST)

            if not created_at:
                return Response({
                    'error': 'No created_at found in response'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Process transcription
            processor = SpeechProcessor()
            response_text = processor.process_text(transcription)
            audio_path = processor.generate_speech(response_text)

            # Prepare response data
            response_data = {
                'response_id': uuid_obj,
                'request_text': transcription,
                'response_text': response_text,
                'audio_link': request.build_absolute_uri(f"{settings.MEDIA_URL}{audio_path}") if audio_path else None,
                'is_successful': bool(audio_path),
                'created_at': created_at
            }

            # Serialize and return response
            serializer = AIProcessSerializer(data=response_data)
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValueError:
            return Response({
                'error': 'Invalid UUID format'
            }, status=status.HTTP_400_BAD_REQUEST)
        except requests.RequestException as e:
            return Response({
                'error': f'Error fetching transcription: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                'error': f'Processing error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)