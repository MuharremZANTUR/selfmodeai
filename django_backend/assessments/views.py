from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Max
from .models import LifeWheelAssessment
from .serializers import LifeWheelAssessmentSerializer, AssessmentCreateSerializer

class LifeWheelAssessmentViewSet(viewsets.ModelViewSet):
    queryset = LifeWheelAssessment.objects.all()
    serializer_class = LifeWheelAssessmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return LifeWheelAssessment.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AssessmentCreateSerializer
        return LifeWheelAssessmentSerializer
    
    def perform_create(self, serializer):
        # Test numarasını otomatik belirle
        last_test = LifeWheelAssessment.objects.filter(
            user=self.request.user
        ).aggregate(Max('test_number'))['test_number__max']
        
        test_number = (last_test or 0) + 1
        serializer.save(user=self.request.user, test_number=test_number)
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """En son değerlendirmeyi getir"""
        latest_assessment = self.get_queryset().order_by('-created_at').first()
        if latest_assessment:
            serializer = self.get_serializer(latest_assessment)
            return Response(serializer.data)
        return Response({'error': 'Henüz değerlendirme bulunamadı'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Tüm değerlendirme geçmişini getir"""
        assessments = self.get_queryset().order_by('-created_at')
        serializer = self.get_serializer(assessments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def progress(self, request):
        """İlerleme analizi yap"""
        assessments = self.get_queryset().order_by('created_at')
        if assessments.count() < 2:
            return Response({'error': 'İlerleme analizi için en az 2 değerlendirme gerekli'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Son iki değerlendirmeyi al
        current = assessments.last()
        previous = assessments[assessments.count()-2]
        
        progress_data = {
            'current': self.get_serializer(current).data,
            'previous': self.get_serializer(previous).data,
            'improvements': {}
        }
        
        # Her alan için iyileşme hesapla
        fields = ['career', 'health', 'relationships', 'personal_growth', 'finances', 'home', 'fun', 'spirituality']
        for field in fields:
            current_score = getattr(current, field)
            previous_score = getattr(previous, field)
            improvement = current_score - previous_score
            progress_data['improvements'][field] = {
                'current': current_score,
                'previous': previous_score,
                'improvement': improvement,
                'percentage': round((improvement / 10) * 100, 1) if previous_score > 0 else 0
            }
        
        return Response(progress_data)
