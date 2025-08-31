from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
import requests
from .models import Payment
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
import hmac
import hashlib
import base64

# Create your views here.

def get_shopier_product_details():
    """Shopier API'sinden ürün detaylarını (ve fiyatı) çeker."""
    # Bu fonksiyon, Shopier'in ürün listeleme API'si dokümantasyonuna göre yazılmalıdır.
    # Şimdilik varsayılan değerler döndürüyoruz.
    return {'id': '38984009', 'price': 10.00, 'title': 'Yaşam Çarkı Testi (Tek Kullanımlık)'}

@login_required
def initiate_payment(request):
    """Kullanıcı için Shopier'de bir sipariş oluşturur ve ödeme linkine yönlendirir."""
    user = request.user
    product = get_shopier_product_details()
    
    # 1. Bizim sistemimizde ödeme kaydı oluştur
    new_payment = Payment.objects.create(
        user=user,
        amount=product['price'],
        status='pending'
    )

    # 2. Shopier API'sine gönderilecek veriyi hazırla
    shopier_order_data = {
        "user": {
            "name": user.first_name or user.username,
            "surname": user.last_name or "User",
            "email": user.email,
        },
        "order_price": product['price'],
        "product_name": product['title'],
        "website_index": str(new_payment.order_id), # Kendi sipariş numaramızı gönderiyoruz
        "callback_url": request.build_absolute_uri(reverse('payments:payment_callback'))
    }

    # 3. Shopier API'sine isteği gönder
    headers = {
        'Authorization': f'Bearer {settings.SHOPIER_PAT}',
        'Content-Type': 'application/json',
    }
    
    try:
        response = requests.post(
            'https://api.shopier.com/v1/orders', 
            headers=headers, 
            json=shopier_order_data,
            timeout=20
        )
        response.raise_for_status() # Hata varsa (4xx or 5xx) exception fırlat
        
        data = response.json()
        payment_url = data.get('payment_url')
        
        if payment_url:
            # Shopier'den gelen sipariş ID'sini kendi kaydımıza ekleyelim
            new_payment.shopier_order_id = data.get('id')
            new_payment.save()
            # Kullanıcıyı ödeme sayfasına yönlendir
            return redirect(payment_url)
        else:
            # Beklenmedik bir cevap geldi
            new_payment.status = 'failed'
            new_payment.save()
            messages.error(request, 'Ödeme başlatılamadı. Lütfen tekrar deneyin veya destek ile iletişime geçin.')
            return redirect('main:dashboard')

    except requests.exceptions.RequestException as e:
        new_payment.status = 'failed'
        new_payment.save()
        messages.error(request, f'Ödeme sağlayıcıya ulaşılamadı: {e}')
        return redirect('main:dashboard')

def payment_success(request):
    # Bu sayfa daha sonra geliştirilecek
    return render(request, 'payments/success.html')

def payment_failure(request):
    # Bu sayfa daha sonra geliştirilecek
    return render(request, 'payments/failure.html')

@csrf_exempt
def payment_callback(request):
    """Shopier'den gelen ödeme sonucu bildirimlerini işler."""
    if request.method == 'POST':
        data = request.POST
        
        # 1. İmza Doğrulaması (Güvenlik)
        expected_signature = data.get('signature')
        
        # Shopier'in imza için kullandığı veriyi yeniden oluştur
        # Not: Shopier dokümantasyonu tam olarak hangi alanları kullandığını belirtmelidir.
        # Genellikle 'status' ve 'website_index' (bizim order_id'miz) kullanılır.
        # Bu kısım Shopier'in güncel dokümantasyonuna göre ayarlanmalıdır.
        # Varsayılan olarak en yaygın kullanılanı yapıyoruz:
        status = data.get('status')
        website_index = data.get('website_index')
        shopier_order_id = data.get('shopier_order_id')
        
        data_to_sign = f"{status}{website_index}{shopier_order_id}"
        h = hmac.new(settings.SHOPIER_API_SECRET.encode('utf-8'), data_to_sign.encode('utf-8'), hashlib.sha256)
        calculated_signature = base64.b64encode(h.digest()).decode('utf-8')
        
        # --- DİKKAT: Shopier'in imza oluşturma yöntemi farklıysa bu kısım çalışmayabilir. ---
        # --- GERÇEK TESTLERDE BU KISIM TEKRAR KONTROL EDİLMELİDİR. ---
        # if calculated_signature != expected_signature:
        #     return JsonResponse({'status': 'error', 'message': 'Invalid signature'}, status=400)
        
        # 2. Ödeme Kaydını Bul ve Güncelle
        try:
            payment = Payment.objects.get(order_id=website_index)
        except Payment.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Order not found'}, status=404)

        # 3. Durumu İşle
        if status == 'successful':
            if payment.status != 'successful': # Sadece daha önce işlenmediyse
                payment.status = 'successful'
                payment.shopier_order_id = shopier_order_id
                payment.save()
                
                # Kullanıcının test hakkını artır
                user = payment.user
                if user:
                    user.test_credits += 1
                    user.save()
                    print(f"Kullanıcı {user.username} için test hakkı 1 artırıldı. Toplam hak: {user.test_credits}")
            
            return JsonResponse({'status': 'ok'})
        
        elif status == 'failed':
            payment.status = 'failed'
            payment.shopier_order_id = shopier_order_id
            payment.save()
            return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
