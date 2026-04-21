# 🩺 GPT Sanal Doktor Asistanı

Bu proje, OpenAI'nin GPT dil modelini ve LangChain kütüphanesini kullanarak hastaların genel şikayetlerini dinleyen ve onlara tıbbi altyapı çerçevesinde ilk yardım seviyesinde (acil durum filtreleri gözetilerek) nazik, kişiselleştirilmiş rehberlik sunan bir asistan API platformudur.

Kullanıcı etkileşimlerini hem terminal üzerinden hem de zengin "Glassmorphism" tasarımlı güzel ve modern bir Web arayüzü üzerinden destekler.

## 🌟 Özellikler

*   **FastAPI & LangChain Entegrasyonu**: Yüksek performanslı asenkron API ve sohbet tabanlı zincir yapısı.
*   **Hafıza (Memory) Yönetimi**: Uygulamaya bağlanan her kullanıcının sohbet verisini ("name" argümanına dayalı olarak) kendi içinde saklayarak diyalog bağlamını sürdürebilir.
*   **Modern Web Arayüzü**: Glassmorphism (şeffaf ve modern form) detaylarına sahip şık bir UI sayfası.
*   **Markdown Çıktı Çözümleme**: Hastaya gönderilen yanıtlar başlıklar, önem belirten kalın yazılar ve liste formatlarında okunabilir düzeyde web arayüzüne taşınır.
*   **Güvenlik Filtresi**: Uygulama "Acil Durum" bulguları hissedildiğinde uyarı vermeye programlı bir ilk asistan mantığında tasarlanmıştır.

## 🛠️ Kurulum ve Çalıştırma

### 1- Repoyu İndirin
```bash
git clone https://github.com/Meszn/GPT_doktor_asistani.git
cd GPT_doktor_asistani
```

### 2- Gerekli Kütüphaneleri Yükleyin
Proje dizininde bir sanal ortam (virtual environment) açmanız önerilir.

```bash
pip install -r requirements.txt
```

### 3- Çevresel Değişkenleri (Environment Variables) Ayarlayın
Kök dizinde bir `.env` dosyası oluşturun ve içerisine kendi OpenAI API anahtarınızı aşağıdaki gibi ekleyin:

```env
OPENAI_API_KEY=sk-gizlianahtariniziburyayaziniz
```
> **Not:** `.env` dosyası repoda bulunmamaktadır, veri güvenliği amacıyla git sisteminden dışlanmıştır (ignored).

### 4- Sunucuyu Başlatın
Uvicorn kullanarak FastAPI sunucunuzu çalıştırın:

```bash
uvicorn doctor_assistant_api:app --reload
```
Bu adımla birlikte sunucunuz `http://127.0.0.1:8000` adresinde hayat bulacaktır.

## 🌐 Web Arayüzü (UI) Başlangıcı
Uygulama çalıştıktan sonra web tarayıcınızı açıp asistanı kullanmaya başlamak için ziyaret edeceğiniz adres:

🔗 **http://127.0.0.1:8000/ui**

**Karşılama Ekranı**: Modal üzerinden İsminizi ve Yaşınızı girdiğinizde, asistan yaşınız ve kimliğinize hitap ederek sizinle konuşmaya başlar.

## 🏗️ Proje Yapısı

*   `doctor_assistant_api.py`: FastAPI ile tasarlanmış, Chat endpoints ve CORS/Static ayarlamalarını içeren ana Backend modülü.
*   `doctor_assistant_terminal.py`: Terminal temelli asistan konuşması demosu oluşturmak için alternatif script.
*   `client_test.py`: API uçlarına JSON tabanlı istek atıp testler yapmak için bir istemci betiği.
*   `static/`: Arka plana bağlı çalışan UI dosyalarımız (`index.html`, `style.css`, `script.js`).

## ⚠️ Yasal Uyarı
Bu proje yalnızca **eğitim ve hobi amaçlı** geliştirilmiştir. Modelin ürettiği metinler ya da çıktılar hiçbir şekilde gerçek doktor teşhisi ya da tedavi ikamesi olarak kullanılamaz. Gerçek tıbbi destek için daima sağlık profesyonellerine (112, vb.) dıyaloğa girilmelidir.
