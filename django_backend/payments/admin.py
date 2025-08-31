from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'amount', 'status', 'created_at', 'shopier_order_id')
    list_filter = ('status', 'created_at')
    search_fields = ('order_id', 'user__username', 'shopier_order_id')
    readonly_fields = ('created_at', 'updated_at')
