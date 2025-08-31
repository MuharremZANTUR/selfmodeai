from django.db import models
from django.conf import settings

class LifeWheelAssessment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assessments')
    test_number = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    # Profil Bilgileri
    employment_status = models.CharField(max_length=50, default='employed')
    marital_status = models.CharField(max_length=50, default='single')
    profession = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)

    # Yeni eklenen profil bilgileri
    age_range = models.CharField(max_length=20, default='25-34', verbose_name="Yaş Aralığı")
    living_area = models.CharField(max_length=20, default='city', verbose_name="Yaşam Alanı")
    children_status = models.CharField(max_length=10, default='none', verbose_name="Çocuk Durumu")
    education_level = models.CharField(max_length=20, default='bachelor', verbose_name="Eğitim Seviyesi")

    # Güncellenmiş 10 Yaşam Alanı
    personal_growth = models.PositiveIntegerField(default=5)
    fun = models.PositiveIntegerField(default=5) # hobi/eğlence
    relationships = models.PositiveIntegerField(default=5) # ilişki/evlilik
    career = models.PositiveIntegerField(default=5) # iş/kariyer
    social_life = models.PositiveIntegerField(default=5) # Sosyal çevre (YENİ)
    family = models.PositiveIntegerField(default=5) # Aile (YENİ)
    finances = models.PositiveIntegerField(default=5) # Para
    health = models.PositiveIntegerField(default=5) # Sağlık
    sports = models.PositiveIntegerField(default=5) # spor/hareket (YENİ)
    spirituality = models.PositiveIntegerField(default=5) # Maneviyat/Anlam

    # Hedefler (3 ana hedef)
    goal1 = models.CharField(max_length=255, blank=True, verbose_name="1. Hedef")
    goal2 = models.CharField(max_length=255, blank=True, verbose_name="2. Hedef")
    goal3 = models.CharField(max_length=255, blank=True, verbose_name="3. Hedef")

    # Öncelikler
    priorities = models.TextField(blank=True, verbose_name="Öncelikler")

    # Güncellenmiş 10 Hedef Skoru
    target_personal_growth = models.PositiveIntegerField(default=0)
    target_fun = models.PositiveIntegerField(default=0)
    target_relationships = models.PositiveIntegerField(default=0)
    target_career = models.PositiveIntegerField(default=0)
    target_social_life = models.PositiveIntegerField(default=0) # (YENİ)
    target_family = models.PositiveIntegerField(default=0) # (YENİ)
    target_finances = models.PositiveIntegerField(default=0)
    target_health = models.PositiveIntegerField(default=0)
    target_sports = models.PositiveIntegerField(default=0) # (YENİ)
    target_spirituality = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'life_wheel_assessments'
        verbose_name = 'Yaşam Çarkı Değerlendirmesi'
        verbose_name_plural = 'Yaşam Çarkı Değerlendirmeleri'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - Test #{self.test_number} ({self.created_at.strftime("%d.%m.%Y")})'

    def get_current_scores(self):
        return {
            'personal_growth': self.personal_growth, 'fun': self.fun,
            'relationships': self.relationships, 'career': self.career,
            'social_life': self.social_life, 'family': self.family,
            'finances': self.finances, 'health': self.health,
            'sports': self.sports, 'spirituality': self.spirituality,
        }

    def get_target_scores(self):
        return {
            'target_personal_growth': self.target_personal_growth, 'target_fun': self.target_fun,
            'target_relationships': self.target_relationships, 'target_career': self.target_career,
            'target_social_life': self.target_social_life, 'target_family': self.target_family,
            'target_finances': self.target_finances, 'target_health': self.target_health,
            'target_sports': self.target_sports, 'target_spirituality': self.target_spirituality,
        }

    def get_profile_info(self):
        return {
            "İş Durumu": self.employment_status,
            "Medeni Durum": self.marital_status,
            "Meslek": self.profession,
            "Ünvan": self.job_title,
            "Yaş Aralığı": self.age_range,
            "Yaşam Alanı": self.living_area,
            "Çocuk Durumu": self.children_status,
            "Eğitim Seviyesi": self.education_level,
            "Öncelikler": self.priorities,
        }
