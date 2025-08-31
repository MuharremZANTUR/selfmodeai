from django.contrib import admin
from .models import AIReport, GeminiService

@admin.register(AIReport)
class AIReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'assessment', 'report_type', 'test_number', 'created_at']
    list_filter = ['report_type', 'test_number', 'created_at', 'user']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Rapor Bilgileri', {
            'fields': ('user', 'assessment', 'report_type', 'test_number')
        }),
        ('İçerik', {
            'fields': ('markdown_content', 'html_content')
        }),
        ('Tarih Bilgileri', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']

@admin.register(GeminiService)
class GeminiServiceAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Servis Bilgileri', {
            'fields': ('api_key', 'model_name', 'is_active')
        }),
        ('Tarih Bilgileri', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
