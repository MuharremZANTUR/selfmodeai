from rest_framework import serializers
from .models import LifeWheelAssessment
from user_management.serializers import UserSerializer

class LifeWheelAssessmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    current_scores = serializers.SerializerMethodField()
    target_scores = serializers.SerializerMethodField()
    goals = serializers.SerializerMethodField()
    
    class Meta:
        model = LifeWheelAssessment
        fields = [
            'id', 'user', 'test_number', 'career', 'health', 'relationships', 
            'personal_growth', 'finances', 'home', 'fun', 'spirituality',
            'goal1', 'goal2', 'goal3', 'target_career', 'target_health', 
            'target_relationships', 'target_personal_growth', 'target_finances', 
            'target_home', 'target_fun', 'target_spirituality',
            'current_scores', 'target_scores', 'goals', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_current_scores(self, obj):
        return obj.get_current_scores()
    
    def get_target_scores(self, obj):
        return obj.get_target_scores()
    
    def get_goals(self, obj):
        return obj.get_goals()
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class AssessmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeWheelAssessment
        fields = [
            'career', 'health', 'relationships', 'personal_growth', 
            'finances', 'home', 'fun', 'spirituality',
            'goal1', 'goal2', 'goal3', 'target_career', 'target_health', 
            'target_relationships', 'target_personal_growth', 'target_finances', 
            'target_home', 'target_fun', 'target_spirituality'
        ]
