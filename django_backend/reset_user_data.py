import os
import sys
import django

# Django ayarlarını yükle
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'selfmode_backend.settings')
django.setup()

from user_management.models import User
from assessments.models import LifeWheelAssessment
from ai_services.models import AIReport

USER_TO_RESET = "admin@selfmode.app"

def reset_user_data():
    """Belirtilen kullanıcının tüm test ve rapor verilerini siler."""
    try:
        # Kullanıcıyı bul
        user = User.objects.get(username=USER_TO_RESET)
        print(f"Kullanıcı bulundu: {user.username}")

        # İlişkili değerlendirmeleri sil
        assessments_deleted, _ = LifeWheelAssessment.objects.filter(user=user).delete()
        print(f"-> {assessments_deleted} adet Yaşam Çarkı değerlendirmesi silindi.")

        # İlişkili AI raporlarını sil
        reports_deleted, _ = AIReport.objects.filter(user=user).delete()
        print(f"-> {reports_deleted} adet AI raporu silindi.")

        print(f"\n✅ '{USER_TO_RESET}' kullanıcısının tüm test verileri başarıyla sıfırlandı!")

    except User.DoesNotExist:
        print(f"❌ HATA: '{USER_TO_RESET}' adında bir kullanıcı bulunamadı.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Beklenmedik bir hata oluştu: {e}")
        sys.exit(1)

if __name__ == "__main__":
    reset_user_data()


