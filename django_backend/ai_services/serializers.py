from rest_framework import serializers
from .models import AIReport, GeminiService
from user_management.serializers import UserSerializer
from assessments.serializers import LifeWheelAssessmentSerializer

class AIReportSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    assessment = LifeWheelAssessmentSerializer(read_only=True)
    
    class Meta:
        model = AIReport
        fields = [
            'id', 'user', 'assessment', 'report_type', 'test_number',
            'markdown_content', 'html_content', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'assessment', 'created_at', 'updated_at']

class AIReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIReport
        fields = ['assessment', 'report_type', 'test_number']

class GeminiServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeminiService
        fields = ['id', 'api_key', 'model_name', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'api_key': {'write_only': True}
        }
