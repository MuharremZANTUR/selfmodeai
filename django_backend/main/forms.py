from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """Özel User modelimiz için UserCreationForm"""
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Form alanlarını Türkçe yap
        self.fields['username'].label = 'Kullanıcı Adı'
        self.fields['email'].label = 'E-posta'
        self.fields['password1'].label = 'Şifre'
        self.fields['password2'].label = 'Şifre Tekrar'
        
        # Yardım metinleri
        self.fields['username'].help_text = '150 karakter veya daha az. Sadece harf, rakam ve @/./+/-/_ karakterleri.'
        self.fields['email'].help_text = 'Geçerli bir e-posta adresi girin.'
        self.fields['password1'].help_text = 'Şifreniz en az 8 karakter olmalı ve yaygın şifrelerden farklı olmalı.'
        self.fields['password2'].help_text = 'Doğrulama için şifrenizi tekrar girin.'
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu e-posta adresi zaten kullanılıyor.')
        return email
