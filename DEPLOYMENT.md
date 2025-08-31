# 🚀 SelfMode Platform Production Deployment Guide

Bu rehber, SelfMode Platform'u production ortamında çalıştırmak için gerekli adımları açıklar.

## 📋 Gereksinimler

### Sistem Gereksinimleri
- **OS**: Ubuntu 20.04+ / CentOS 8+ / Windows 10+ / macOS 10.15+
- **RAM**: Minimum 4GB, Önerilen 8GB+
- **Disk**: Minimum 20GB boş alan
- **CPU**: 2+ çekirdek

### Yazılım Gereksinimleri
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Git**: 2.25+

## 🔧 Kurulum Adımları

### 1. Projeyi Klonlayın
```bash
git clone https://github.com/yourusername/selfmode-platform.git
cd selfmode-platform
```

### 2. Environment Variables Ayarlayın
`backend/env.production` dosyasını düzenleyin:

```bash
# Database Configuration
DB_HOST=your_production_db_host
DB_PORT=3306
DB_USER=your_production_db_user
DB_PASSWORD=your_secure_password_here
DB_NAME=selfmode_db

# Server Configuration
PORT=5000
NODE_ENV=production

# JWT Configuration (DEĞİŞTİRİN!)
JWT_SECRET=your_super_secret_production_jwt_key_here
JWT_EXPIRES_IN=7d

# Frontend URL (DOMAIN'İNİZİ GİRİN)
FRONTEND_URL=https://yourdomain.com

# iyzico Configuration (Production)
IYZICO_API_KEY=your_production_iyzico_api_key
IYZICO_SECRET_KEY=your_production_iyzico_secret_key
IYZICO_BASE_URL=https://api.iyzipay.com
```

### 3. Domain Ayarlayın
Nginx konfigürasyonunda domain'inizi güncelleyin:

```bash
# nginx/nginx.conf dosyasında
server_name yourdomain.com www.yourdomain.com;
```

## 🐳 Docker ile Deployment

### Otomatik Deployment (Önerilen)

#### Linux/macOS
```bash
chmod +x deploy-production.sh
./deploy-production.sh
```

#### Windows PowerShell
```powershell
.\deploy-production.ps1
```

### Manuel Deployment
```bash
# Gerekli dizinleri oluşturun
mkdir -p logs/nginx nginx/ssl mysql/init

# Servisleri başlatın
docker-compose up -d --build

# Logları kontrol edin
docker-compose logs -f
```

## 🔒 SSL Sertifikası Kurulumu

### Let's Encrypt ile Ücretsiz SSL

1. **Certbot Kurulumu**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install certbot

# CentOS/RHEL
sudo yum install certbot
```

2. **Sertifika Oluşturma**
```bash
sudo certbot certonly --standalone -d yourdomain.com
```

3. **Sertifikaları Kopyalama**
```bash
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem
sudo chown -R $USER:$USER nginx/ssl/
```

4. **Otomatik Yenileme**
```bash
# Crontab'a ekleyin
sudo crontab -e

# Her gün gece yarısı yenileme
0 0 * * * /usr/bin/certbot renew --quiet --post-hook "docker-compose restart nginx"
```

## 🌐 Domain ve DNS Ayarları

### A Record
```
yourdomain.com     →  YOUR_SERVER_IP
www.yourdomain.com →  YOUR_SERVER_IP
```

### CNAME Record (Opsiyonel)
```
api.yourdomain.com →  yourdomain.com
```

## 📊 Monitoring ve Logs

### Servis Durumu Kontrolü
```bash
# Tüm servislerin durumu
docker-compose ps

# Backend health check
curl http://localhost:5000/api/health

# Nginx health check
curl http://localhost/health
```

### Logları İzleme
```bash
# Tüm servisler
docker-compose logs -f

# Sadece backend
docker-compose logs -f backend

# Sadece nginx
docker-compose logs -f nginx

# Sadece database
docker-compose logs -f mysql
```

### Performans İzleme
```bash
# Container kaynak kullanımı
docker stats

# Disk kullanımı
docker system df
```

## 🔧 Bakım ve Güncelleme

### Güncelleme
```bash
# Kodu güncelleyin
git pull origin main

# Servisleri yeniden başlatın
docker-compose down
docker-compose up -d --build
```

### Backup
```bash
# Database backup
docker-compose exec mysql mysqldump -u root -p selfmode_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Tüm veri backup
docker run --rm -v selfmode-platform_mysql_data:/data -v $(pwd):/backup alpine tar czf /backup/mysql_backup_$(date +%Y%m%d_%H%M%S).tar.gz -C /data .
```

### Temizlik
```bash
# Kullanılmayan Docker kaynakları
docker system prune -a

# Eski logları temizleme
docker-compose exec nginx find /var/log/nginx -name "*.log" -mtime +30 -delete
```

## 🚨 Güvenlik Kontrol Listesi

- [ ] JWT_SECRET değiştirildi
- [ ] Database şifresi güçlü
- [ ] SSL sertifikası kuruldu
- [ ] Firewall ayarlandı (port 80, 443, 22 açık)
- [ ] Rate limiting aktif
- [ ] Security headers aktif
- [ ] Database root erişimi kısıtlandı
- [ ] Regular backup planı
- [ ] Monitoring ve alerting kuruldu

## 🆘 Sorun Giderme

### Yaygın Sorunlar

#### 1. Port Çakışması
```bash
# Port kullanımını kontrol edin
netstat -tulpn | grep :5000

# Servisi durdurun
docker-compose down
```

#### 2. Database Bağlantı Hatası
```bash
# Database loglarını kontrol edin
docker-compose logs mysql

# Database container'ını yeniden başlatın
docker-compose restart mysql
```

#### 3. SSL Sertifika Hatası
```bash
# Sertifika geçerliliğini kontrol edin
openssl x509 -in nginx/ssl/cert.pem -text -noout

# Nginx konfigürasyonunu test edin
docker-compose exec nginx nginx -t
```

#### 4. Memory/CPU Sorunları
```bash
# Kaynak kullanımını kontrol edin
docker stats

# Container limitlerini ayarlayın (docker-compose.yml)
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
```

## 📞 Destek

- **GitHub Issues**: [Proje Repository](https://github.com/yourusername/selfmode-platform)
- **Email**: support@yourdomain.com
- **Documentation**: [API Docs](https://yourdomain.com/api/docs)

## 📝 Changelog

### v1.0.1
- Production deployment scripts eklendi
- Docker ve Nginx konfigürasyonu
- SSL sertifika desteği
- Monitoring ve logging iyileştirmeleri

### v1.0.0
- İlk production release
- Temel kariyer analiz platformu
- iyzico ödeme entegrasyonu
- Admin paneli

---

**Not**: Bu deployment guide sürekli güncellenmektedir. En güncel versiyon için GitHub repository'yi kontrol edin.
