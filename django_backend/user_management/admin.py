
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profil Bilgileri'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'has_payment', 'payment_date', 'is_active')
    list_filter = ('has_payment', 'is_active', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Ödeme Bilgileri', {'fields': ('has_payment', 'payment_date')}),
        ('Kişisel Bilgiler', {'fields': ('phone', 'birth_date')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Kişisel Bilgiler', {'fields': ('phone', 'birth_date')}),
    )

admin.site.register(User, CustomUserAdmin)
