from django.db import models
from user_management.models import User
from assessments.models import LifeWheelAssessment

class AIReport(models.Model):
    """AI tarafından oluşturulan raporlar"""
    REPORT_TYPES = [
        ('initial', 'İlk Değerlendirme'),
        ('progress', 'İlerleme Raporu'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_reports')
    assessment = models.ForeignKey(LifeWheelAssessment, on_delete=models.CASCADE, related_name='ai_reports')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES, default='initial')
    test_number = models.IntegerField(default=1)
    
    # AI rapor içeriği
    markdown_content = models.TextField()
    html_content = models.TextField(blank=True)
    
    # Rapor metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ai_reports'
        verbose_name = 'AI Raporu'
        verbose_name_plural = 'AI Raporları'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.get_report_type_display()} (Test {self.test_number})"

class GeminiService(models.Model):
    """Gemini AI servis ayarları"""
    api_key = models.CharField(max_length=500)
    model_name = models.CharField(max_length=100, default='gemini-1.5-pro')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'gemini_service'
        verbose_name = 'Gemini AI Servisi'
        verbose_name_plural = 'Gemini AI Servisleri'
    
    def __str__(self):
        return f"Gemini AI - {self.model_name}"
