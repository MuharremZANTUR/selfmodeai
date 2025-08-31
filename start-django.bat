@echo off
title SelfMode Platform - Django Server
color 0A

echo.
echo ========================================
echo    SELFMODE PLATFORM DJANGO SERVER
echo ========================================
echo.

echo [1/3] Port kontrolü yapılıyor...
netstat -ano | findstr :8000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ Port 8000 (Django) zaten kullanımda!
    echo Mevcut process'leri sonlandırılıyor...
    taskkill /f /im python.exe >nul 2>&1
    timeout /t 2 >nul
)

echo ✅ Port 8000 temizlendi
echo.

echo [2/3] Django backend başlatılıyor...
cd /d %~dp0django_backend
call venv\Scripts\activate.bat

echo [3/3] Django server başlatılıyor...
echo 🌐 Ana Sayfa: http://localhost:8000
echo 📊 Admin Panel: http://localhost:8000/admin
echo 🔧 API Endpoints: http://localhost:8000/api/
echo.
python manage.py runserver 0.0.0.0:8000

pause
