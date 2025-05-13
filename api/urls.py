from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AudioFileViewSet, AIProcessViewSet

router = DefaultRouter()
router.register(r'audio', AudioFileViewSet)
router.register(r'audio/ai-process', AIProcessViewSet, basename='ai-process')

urlpatterns = [
    path('', include(router.urls)),
]