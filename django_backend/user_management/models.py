from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """Genişletilmiş kullanıcı modeli"""
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    has_payment = models.BooleanField(default=False)
    payment_date = models.DateTimeField(blank=True, null=True)
    
    # İş modeli için yeni alanlar
    test_credits = models.PositiveIntegerField(default=1, verbose_name="Test Hakkı")
    tests_completed = models.PositiveIntegerField(default=0, verbose_name="Tamamlanan Test Sayısı")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class UserProfile(models.Model):
    """Kullanıcı profil bilgileri"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profession = models.CharField(max_length=100, blank=True)
    current_job = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'Kullanıcı Profili'
        verbose_name_plural = 'Kullanıcı Profilleri'
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} Profili"
