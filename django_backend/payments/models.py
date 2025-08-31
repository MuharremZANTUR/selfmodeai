from django.db import models
from django.conf import settings
import uuid

class Payment(models.Model):
    """Shopier ödeme işlemlerini takip eden model."""
    
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('successful', 'Başarılı'),
        ('failed', 'Başarısız'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kullanıcı")
    order_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4, verbose_name="Sipariş ID")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tutar")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Durum")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")
    
    shopier_order_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Shopier Sipariş ID")
    
    class Meta:
        verbose_name = "Ödeme"
        verbose_name_plural = "Ödemeler"
        ordering = ['-created_at']

    def __str__(self):
        return f"Sipariş {self.order_id} - {self.user.username if self.user else 'Bilinmeyen Kullanıcı'} - {self.get_status_display()}"
