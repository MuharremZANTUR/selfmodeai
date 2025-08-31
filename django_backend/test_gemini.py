#!/usr/bin/env python
"""
Gemini API Test Script
"""
import os
import sys
import django

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'selfmode_backend.settings')
django.setup()

from django.conf import settings
import google.generativeai as genai

def test_gemini_api():
    """Gemini API'yi test et"""
    try:
        print("🔍 Gemini API Test Ediliyor...")
        print(f"API Key: {settings.GEMINI_API_KEY[:20]}...")
        
        # Gemini AI konfigürasyonu
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Basit bir test prompt'u
        prompt = """
        Merhaba! Sen bir yaşam koçusun. 
        Kısa bir motivasyon mesajı yaz (2-3 cümle).
        """
        
        print("📝 Test prompt'u gönderiliyor...")
        response = model.generate_content(prompt)
        
        print("✅ Gemini API Başarılı!")
        print("🤖 AI Yanıtı:")
        print("-" * 50)
        print(response.text)
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Gemini API Hatası: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_gemini_api()
    if success:
        print("\n🎉 Gemini API Test Başarılı!")
    else:
        print("\n💥 Gemini API Test Başarısız!")
        sys.exit(1)
