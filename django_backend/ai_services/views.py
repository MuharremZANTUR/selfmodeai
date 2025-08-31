from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
import google.generativeai as genai
from .models import AIReport, GeminiService
from .serializers import AIReportSerializer, AIReportCreateSerializer
from assessments.models import LifeWheelAssessment

class AIReportViewSet(viewsets.ModelViewSet):
    queryset = AIReport.objects.all()
    serializer_class = AIReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return AIReport.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AIReportCreateSerializer
        return AIReportSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def generate_initial_report(self, request):
        """İlk değerlendirme raporu oluştur"""
        try:
            assessment_id = request.data.get('assessment_id')
            assessment = LifeWheelAssessment.objects.get(id=assessment_id, user=request.user)
            
            # Gemini AI ile rapor oluştur
            report_content = self._generate_ai_report(assessment, 'initial')
            
            # Raporu kaydet
            ai_report = AIReport.objects.create(
                user=request.user,
                assessment=assessment,
                report_type='initial',
                test_number=assessment.test_number,
                markdown_content=report_content
            )
            
            serializer = AIReportSerializer(ai_report)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except LifeWheelAssessment.DoesNotExist:
            return Response({'error': 'Değerlendirme bulunamadı'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Rapor oluşturulamadı: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def generate_progress_report(self, request):
        """İlerleme raporu oluştur"""
        try:
            current_assessment_id = request.data.get('current_assessment_id')
            previous_assessment_id = request.data.get('previous_assessment_id')
            
            current_assessment = LifeWheelAssessment.objects.get(id=current_assessment_id, user=request.user)
            previous_assessment = LifeWheelAssessment.objects.get(id=previous_assessment_id, user=request.user)
            
            # Gemini AI ile ilerleme raporu oluştur
            report_content = self._generate_progress_report(current_assessment, previous_assessment)
            
            # Raporu kaydet
            ai_report = AIReport.objects.create(
                user=request.user,
                assessment=current_assessment,
                report_type='progress',
                test_number=current_assessment.test_number,
                markdown_content=report_content
            )
            
            serializer = AIReportSerializer(ai_report)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except LifeWheelAssessment.DoesNotExist:
            return Response({'error': 'Değerlendirme bulunamadı'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Rapor oluşturulamadı: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _generate_ai_report(self, assessment, report_type):
        """Gemini AI ile rapor oluştur"""
        try:
            # Gemini AI konfigürasyonu
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            # Prompt oluştur
            prompt = self._create_prompt(assessment, report_type)
            
            # AI'dan yanıt al
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"AI raporu oluşturulamadı: {str(e)}"
    
    def _create_prompt(self, assessment, report_type):
        """AI prompt'u oluştur"""
        current_scores = assessment.get_current_scores()
        target_scores = assessment.get_target_scores()
        goals = assessment.get_goals()
        
        if report_type == 'initial':
            return f"""
            Yaşam Çarkı Analiz Raporu oluştur:
            
            Mevcut Skorlar: {current_scores}
            Hedef Skorlar: {target_scores}
            Hedefler: {goals}
            
            Detaylı, motive edici ve kişiselleştirilmiş bir rapor hazırla.
            """
        else:
            return f"""
            İlerleme Raporu oluştur:
            
            Mevcut Durum: {current_scores}
            Hedefler: {target_scores}
            
            İlerleme analizi ve öneriler içeren bir rapor hazırla.
            """
    
    def _generate_progress_report(self, current_assessment, previous_assessment):
        """İlerleme raporu için prompt oluştur"""
        current_scores = current_assessment.get_current_scores()
        previous_scores = previous_assessment.get_current_scores()
        
        return f"""
        İlerleme Raporu:
        
        Önceki Skorlar: {previous_scores}
        Mevcut Skorlar: {current_scores}
        
        İyileşme alanları ve öneriler içeren detaylı bir rapor hazırla.
        """
