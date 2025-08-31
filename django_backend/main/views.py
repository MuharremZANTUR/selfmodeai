from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from assessments.models import LifeWheelAssessment
from ai_services.models import AIReport
import json

def home(request):
    """Ana sayfa"""
    return render(request, 'main/home.html')

def register_view(request):
    """Kullanıcı kayıt sayfası"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Kullanıcıyı otomatik giriş yap
            login(request, user)
            messages.success(request, 'Hesabınız başarıyla oluşturuldu!')
            return redirect('main:dashboard')
        else:
            messages.error(request, 'Kayıt sırasında hata oluştu. Lütfen tekrar deneyin.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    """Kullanıcı dashboard'u"""
    user = request.user
    recent_assessments = LifeWheelAssessment.objects.filter(user=user).order_by('-created_at')[:5]
    recent_reports = AIReport.objects.filter(user=user).order_by('-created_at')[:5]

    # Karşılaştırma grafiği için son 3 testi hazırla
    comparison_assessments = recent_assessments[:3]
    comparison_data = {
        "labels": [
            'İş/Kariyer', 'Sağlık', 'İlişki/Evlilik', 'Kişisel Gelişim', 'Para', 
            'Hobi/Eğlence', 'Maneviyat/Anlam', 'Sosyal Çevre', 
            'Aile (Ebeveyn, Kardeş)', 'Spor/Hareket'
        ],
        "datasets": []
    }
    
    colors = [
        {'bg': 'rgba(33, 37, 41, 0.5)',   'border': 'rgba(33, 37, 41, 1)'},    # Siyah - Test 1 (En eski)
        {'bg': 'rgba(13, 110, 253, 0.5)', 'border': 'rgba(13, 110, 253, 1)'},    # Mavi - Test 2
        {'bg': 'rgba(25, 135, 84, 0.5)',  'border': 'rgba(25, 135, 84, 1)'},     # Yeşil - Test 3
        {'bg': 'rgba(255, 193, 7, 0.5)',  'border': 'rgba(255, 193, 7, 1)'}      # Sarı - Test 4 (En yeni)
    ]

    # En son testin hedeflerini ekle
    if comparison_assessments:
        latest_assessment = comparison_assessments[0]
        target_dataset = {
            "label": f"Hedef ({latest_assessment.created_at.strftime('%d.%m.%Y')})",
            "data": list(latest_assessment.get_target_scores().values()),
            "backgroundColor": "transparent",
            "borderColor": "rgba(220, 53, 69, 1)", # Kırmızı - Hedef
            "borderWidth": 0 # Eklentiyle çizildiği için 0 kalmalı
        }
        comparison_data["datasets"].append(target_dataset)

    # Son 4 testi (veya daha azını) ekle, en eskiden en yeniye doğru sırala
    sorted_assessments = sorted(comparison_assessments[:4], key=lambda x: x.test_number)
    for i, assessment in enumerate(sorted_assessments):
        dataset = {
            "label": f"Test #{assessment.test_number} ({assessment.created_at.strftime('%d.%m.%Y')})",
            "data": list(assessment.get_current_scores().values()),
            "backgroundColor": colors[i]['bg'],
            "borderColor": colors[i]['border'],
            "borderWidth": 2
        }
        comparison_data["datasets"].append(dataset)
    
    # Her değerlendirme için ortalama skor hesapla (Liste için)
    for assessment in recent_assessments:
        total_score = sum(assessment.get_current_scores().values())
        assessment.average_score = round(total_score / 8, 1)
        
    # --- Gelişim Özet Tablosu için Veri Hazırlama ---
    summary_data = []
    life_areas = [
        ('İş/Kariyer', 'career', 'Mesleki tatmin, kariyer hedefleri ve iş-yaşam dengesi.'),
        ('Sağlık', 'health', 'Fiziksel zindelik, enerji seviyesi ve genel sağlık durumu.'),
        ('İlişki/Evlilik', 'relationships', 'Partnerle olan duygusal bağ, iletişim ve paylaşılan zaman.'),
        ('Kişisel Gelişim', 'personal_growth', 'Yeni şeyler öğrenme, beceri kazanma ve kendini gerçekleştirme.'),
        ('Para', 'finances', 'Finansal güvenlik, gelir yönetimi ve para ile olan ilişki.'),
        ('Hobi/Eğlence', 'fun', 'Keyif alınan aktiviteler, dinlenme ve kendine zaman ayırma.'),
        ('Maneviyat/Anlam', 'spirituality', 'Hayatın amacı, içsel huzur ve değerlerle uyumlu yaşama.'),
        ('Sosyal Çevre', 'social_life', 'Arkadaşlar, sosyal etkileşimler ve topluluk içindeki yer.'),
        ('Aile (Ebeveyn, Kardeş)', 'family', 'Kök aile ile olan ilişkiler, iletişim ve destek.'),
        ('Spor/Hareket', 'sports', 'Düzenli fiziksel aktivite, vücut esnekliği ve hareketlilik.'),
    ]
    
    # Kullanıcının ilk 4 testini al
    user_assessments = LifeWheelAssessment.objects.filter(user=user, test_number__in=[1, 2, 3, 4]).order_by('test_number')
    
    assessment_map = {a.test_number: a for a in user_assessments}
    test_1 = assessment_map.get(1)
    
    if test_1: # Sadece en az 1 test yapıldıysa tabloyu oluştur
        latest_test = user_assessments.last()
        
        for area_display, area_key, area_description in life_areas:
            row = {'area': area_display, 'description': area_description}
            
            # Test ve hedef skorlarını al
            test_1_score = getattr(test_1, area_key, None)
            target_score = getattr(test_1, f'target_{area_key}', None)
            latest_score = getattr(latest_test, area_key, None)
            
            row['test_1_score'] = test_1_score
            row['target_score'] = target_score
            row['test_2_score'] = getattr(assessment_map.get(2), area_key, None)
            row['test_3_score'] = getattr(assessment_map.get(3), area_key, None)
            row['test_4_score'] = getattr(assessment_map.get(4), area_key, None)
            
            summary_data.append(row)

    context = {
        'recent_assessments': recent_assessments,
        'recent_reports': recent_reports,
        'comparison_data': json.dumps(comparison_data),
        'summary_data': summary_data,
    }
    return render(request, 'main/dashboard.html', context)

@login_required
def life_wheel(request):
    """Yaşam çarkı sayfası - İş modeli mantığı eklendi"""
    user = request.user
    
    # Kullanıcının test hakkı var mı?
    can_take_test = user.test_credits > user.tests_completed
    is_first_test = user.tests_completed == 0

    if request.method == 'POST':
        # Post ederken de hakkı var mı diye kontrol et
        if not can_take_test:
            messages.error(request, 'Yeni bir değerlendirme yapmak için test hakkınız bulunmamaktadır.')
            return redirect('main:dashboard')

        next_test_number = user.tests_completed + 1
        
        # Gelen verilerle testi oluştur/güncelle
        test_data = { 'user': user, 'test_number': next_test_number }
        life_areas_keys = [
            'career', 'health', 'relationships', 'personal_growth', 
            'finances', 'fun', 'spirituality', 'social_life', 'family', 'sports'
        ]

        for area_key in life_areas_keys:
            score = request.POST.get(f'test_{next_test_number}_{area_key}')
            if score:
                test_data[area_key] = int(score)
        
        # Sadece 1. test için hedefleri ve profil bilgilerini de al
        if is_first_test:
            test_data['goal1'] = request.POST.get('goal1', '')
            test_data['goal2'] = request.POST.get('goal2', '')
            test_data['goal3'] = request.POST.get('goal3', '')
            test_data['priorities'] = request.POST.get('priorities', '') # Yeni alanı ekle
            # Mevcut profil bilgileri
            test_data['employment_status'] = request.POST.get('employment_status', 'employed')
            test_data['marital_status'] = request.POST.get('marital_status', 'single')
            test_data['profession'] = request.POST.get('profession', '')
            test_data['job_title'] = request.POST.get('job_title', '')
            # Yeni profil bilgileri
            test_data['age_range'] = request.POST.get('age_range', '25-34')
            test_data['living_area'] = request.POST.get('living_area', 'city')
            test_data['children_status'] = request.POST.get('children_status', 'none')
            test_data['education_level'] = request.POST.get('education_level', 'bachelor')
            
            for area_key in life_areas_keys:
                target_score = request.POST.get(f'target_{area_key}')
                if target_score:
                    test_data[f'target_{area_key}'] = int(target_score)

        assessment, created = LifeWheelAssessment.objects.update_or_create(
            user=user, test_number=next_test_number,
            defaults=test_data
        )
        
        # Test hakkını güncelle
        # Yalnızca yeni bir test oluşturulduysa sayacı artır
        if created:
            user.tests_completed += 1
            user.save()
        
        messages.success(request, f'Yaşam çarkı değerlendirmesi #{next_test_number} başarıyla kaydedildi! Kalan Test Hakkınız: {user.test_credits - user.tests_completed}')
        
        # Otomatik AI raporu oluştur
        try:
            from ai_services.views import AIReportViewSet
            ai_viewset = AIReportViewSet()
            ai_viewset.request = request
            ai_viewset.action = 'generate_initial_report'
            
            # AI raporu oluştur
            report_content = ai_viewset._generate_ai_report(assessment, 'initial')
            
            # Raporu kaydet
            from ai_services.models import AIReport
            ai_report = AIReport.objects.create(
                user=request.user,
                assessment=assessment,
                report_type='initial',
                test_number=assessment.test_number,
                markdown_content=report_content
            )
            
            messages.success(request, 'AI raporu otomatik olarak oluşturuldu!')
            return redirect('main:ai_report', report_id=ai_report.id)
            
        except Exception as e:
            messages.warning(request, 'Yaşam çarkı kaydedildi ancak AI raporu oluşturulamadı.')
            return redirect('main:dashboard')
    
    # --- GET isteği için ---
    # Kullanıcının test hakkı var mı?
    if not can_take_test:
        return render(request, 'main/no_credits.html')

    # Sıradaki test numarasını belirle
    next_test_number = user.tests_completed + 1

    # Tablo için danışanın geçmiş verilerini hazırla
    life_areas = [
        ('İş/Kariyer', 'career', 'Mesleki tatmin, kariyer hedefleri ve iş-yaşam dengesi.'),
        ('Sağlık', 'health', 'Fiziksel zindelik, enerji seviyesi ve genel sağlık durumu.'),
        ('İlişki/Evlilik', 'relationships', 'Partnerle olan duygusal bağ, iletişim ve paylaşılan zaman.'),
        ('Kişisel Gelişim', 'personal_growth', 'Yeni şeyler öğrenme, beceri kazanma ve kendini gerçekleştirme.'),
        ('Para', 'finances', 'Finansal güvenlik, gelir yönetimi ve para ile olan ilişki.'),
        ('Hobi/Eğlence', 'fun', 'Keyif alınan aktiviteler, dinlenme ve kendine zaman ayırma.'),
        ('Maneviyat/Anlam', 'spirituality', 'Hayatın amacı, içsel huzur ve değerlerle uyumlu yaşama.'),
        ('Sosyal Çevre', 'social_life', 'Arkadaşlar, sosyal etkileşimler ve topluluk içindeki yer.'),
        ('Aile (Ebeveyn, Kardeş)', 'family', 'Kök aile ile olan ilişkiler, iletişim ve destek.'),
        ('Spor/Hareket', 'sports', 'Düzenli fiziksel aktivite, vücut esnekliği ve hareketlilik.'),
    ]
    user_assessments = LifeWheelAssessment.objects.filter(user=user, test_number__in=[1, 2, 3, 4]).order_by('test_number')
    assessment_map = {a.test_number: a for a in user_assessments}
    
    table_data = []
    for area_display, area_key, area_description in life_areas:
        row = {
            'area_display': area_display,
            'area_key': area_key,
            'description': area_description,
            'test_1_score': getattr(assessment_map.get(1), area_key, ''),
            'target_score': getattr(assessment_map.get(1), f'target_{area_key}', ''),
            'test_2_score': getattr(assessment_map.get(2), area_key, ''),
            'test_3_score': getattr(assessment_map.get(3), area_key, ''),
            'test_4_score': getattr(assessment_map.get(4), area_key, ''),
        }
        table_data.append(row)
    
    context = {
        'is_first_test': is_first_test,
        'next_test_number': next_test_number,
        'table_data': table_data,
    }
    return render(request, 'main/life_wheel.html', context)

@login_required
def assessments(request):
    """Değerlendirmeler sayfası"""
    user = request.user
    user_assessments = LifeWheelAssessment.objects.filter(user=user).order_by('-created_at')
    context = {
        'assessments': user_assessments,
    }
    return render(request, 'main/assessments.html', context)

@login_required
def ai_coach(request):
    """AI koç sayfası"""
    user = request.user
    recent_reports = AIReport.objects.filter(user=user).order_by('-created_at')[:5]
    
    context = {
        'recent_reports': recent_reports,
    }
    return render(request, 'main/ai_coach.html', context)

@login_required
def profile(request):
    """Profil sayfası"""
    user = request.user
    
    # Kullanıcı istatistikleri
    total_assessments = LifeWheelAssessment.objects.filter(user=user).count()
    total_reports = AIReport.objects.filter(user=user).count()
    latest_assessment = LifeWheelAssessment.objects.filter(user=user).order_by('-created_at').first()
    
    # En iyi alanları hesapla
    top_areas = []
    if latest_assessment:
        areas = [
            ('Kariyer', latest_assessment.career),
            ('Sağlık', latest_assessment.health),
            ('İlişkiler', latest_assessment.relationships),
            ('Kişisel Gelişim', latest_assessment.personal_growth),
            ('Finans', latest_assessment.finances),
            ('Ev', latest_assessment.home),
            ('Eğlence', latest_assessment.fun),
            ('Maneviyat', latest_assessment.spirituality)
        ]
        # Skorlara göre sırala ve en iyi 3'ü al
        top_areas = sorted(areas, key=lambda x: x[1], reverse=True)[:3]
    
    context = {
        'total_assessments': total_assessments,
        'total_reports': total_reports,
        'latest_assessment': latest_assessment,
        'top_areas': top_areas,
    }
    return render(request, 'main/profile.html', context)

@login_required
def ai_report_view(request, report_id):
    """AI raporu görüntüleme sayfası"""
    try:
        from ai_services.models import AIReport
        report = AIReport.objects.get(id=report_id, user=request.user)
        context = {
            'report': report,
            'assessment': report.assessment,
        }
        return render(request, 'main/ai_report.html', context)
    except AIReport.DoesNotExist:
        messages.error(request, 'AI raporu bulunamadı.')
        return redirect('main:dashboard')
