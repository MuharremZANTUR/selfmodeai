from django.contrib import admin
from .models import LifeWheelAssessment

@admin.register(LifeWheelAssessment)
class LifeWheelAssessmentAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'test_number', 'career', 'health', 'relationships', 
        'personal_growth', 'finances', 'fun', 'spirituality', 
        'social_life', 'family', 'sports', 'created_at'
    ]
    list_filter = ['test_number', 'created_at', 'user']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Kullanıcı Bilgileri', {
            'fields': ('user', 'test_number')
        }),
        ('Profil Bilgileri', {
            'fields': (
                'employment_status', 'marital_status', 'profession', 
                'job_title', 'age_range', 'living_area', 'children_status', 
                'education_level'
            )
        }),
        ('Mevcut Skorlar', {
            'fields': (
                'career', 'health', 'relationships', 'personal_growth', 
                'finances', 'fun', 'spirituality', 'social_life', 
                'family', 'sports'
            )
        }),
        ('Hedefler ve Öncelikler', {
            'fields': ('goal1', 'goal2', 'goal3', 'priorities')
        }),
        ('Hedef Skorlar', {
            'fields': (
                'target_career', 'target_health', 'target_relationships', 
                'target_personal_growth', 'target_finances', 'target_fun', 
                'target_spirituality', 'target_social_life', 'target_family', 
                'target_sports'
            )
        }),
        ('Tarih Bilgileri', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']
