# 🚀 SelfMode Platform Server Kullanım Kılavuzu

## 📁 Oluşturulan Dosyalar

### 1. `start-servers.bat` - Ana Başlatıcı
- ✅ Backend ve Frontend'i tek seferde başlatır
- ✅ Port çakışmalarını otomatik çözer
- ✅ Her server için ayrı pencere açar
- ✅ Renkli ve bilgilendirici arayüz

### 2. `stop-servers.bat` - Server Durdurucu
- ✅ Tüm serverları güvenli şekilde durdurur
- ✅ Port 5000 ve 3000'i temizler
- ✅ Tüm Node.js process'lerini sonlandırır

### 3. `quick-test.bat` - Hızlı Test
- ✅ Server durumlarını hızlıca test eder
- ✅ Backend, Frontend ve AI endpoint'leri kontrol eder

## 🎯 Kullanım

### 🚀 Serverları Başlatmak
```bash
# Çift tıklayın veya çalıştırın:
start-servers.bat
```

**Ne olur:**
1. Port kontrolü yapılır
2. Çakışan process'ler temizlenir
3. Backend başlatılır (Port 5000)
4. 5 saniye beklenir
5. Frontend başlatılır (Port 3000)
6. Her ikisi için ayrı pencere açılır

### 🛑 Serverları Durdurmak
```bash
# Çift tıklayın veya çalıştırın:
stop-servers.bat
```

**Ne olur:**
1. Port 5000 kontrol edilir ve temizlenir
2. Port 3000 kontrol edilir ve temizlenir
3. Tüm Node.js process'leri sonlandırılır

### 🧪 Hızlı Test
```bash
# Çift tıklayın veya çalıştırın:
quick-test.bat
```

**Ne olur:**
1. Backend durumu test edilir
2. Frontend durumu test edilir
3. AI endpoint erişimi test edilir

## 🌐 Erişim URL'leri

| Servis | URL | Açıklama |
|--------|-----|----------|
| **Frontend** | http://localhost:3000 | Ana uygulama |
| **Backend** | http://localhost:5000 | API sunucusu |
| **Health Check** | http://localhost:5000/api/health | Backend durumu |
| **AI Analiz** | http://localhost:5000/api/ai/analyze-assessment | AI rapor oluşturma |

## 💡 Önemli Notlar

### ✅ Başarılı Başlatma
- Backend: "🚀 SelfMode Backend server is running on port 5000"
- Frontend: "Compiled successfully!" mesajı
- Her ikisi için ayrı pencere açılır

### ❌ Hata Durumları
- **Port çakışması:** Otomatik temizlenir
- **Node.js bulunamadı:** `npm install` çalıştırın
- **Modül bulunamadı:** `npm install` çalıştırın

### 🔧 Sorun Giderme
1. **Serverlar başlamıyorsa:** `stop-servers.bat` çalıştırın, sonra `start-servers.bat`
2. **Port hatası:** `stop-servers.bat` ile temizleyin
3. **Modül hatası:** Backend klasöründe `npm install` çalıştırın

## 🎨 Özellikler

- **Renkli arayüz:** Yeşil (başlatıcı), Kırmızı (durdurucu), Mavi (test)
- **Otomatik port temizleme:** Çakışmaları otomatik çözer
- **Ayrı pencereler:** Her server için ayrı log penceresi
- **Bilgilendirici mesajlar:** Her adımda ne olduğu açıklanır
- **Güvenli durdurma:** Process'leri güvenli şekilde sonlandırır

## 🚀 Hızlı Başlangıç

1. **`start-servers.bat`** çift tıklayın
2. **Tarayıcıda** http://localhost:3000 adresine gidin
3. **"Gemini AI ile Analiz Başlat"** butonunu test edin
4. **Serverları durdurmak için** `stop-servers.bat` kullanın

---

**🎯 Artık tek tıkla tüm serverları başlatabilirsiniz!**
