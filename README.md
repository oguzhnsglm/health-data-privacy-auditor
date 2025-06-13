# 🛡️ Health Data Privacy Auditor

**Health Data Privacy Auditor**, sağlık verilerinin gizliliğini analiz eden ve düzenleyici gerekliliklere uyumunu değerlendiren bir LLM tabanlı denetim aracıdır. Proje kapsamında kullanıcı tarafından yüklenen sağlık veri setleri, yapay zeka desteğiyle analiz edilir ve PII, HIPAA, GDPR, KVKK ve PCI DSS gibi regülasyonlara göre riskli sütunlar belirlenerek temizlenmiş bir veri seti sunulur.

---

## 🎯 Proje Amacı

Sağlık verileri, en hassas kişisel veriler arasında yer alır ve yüksek düzeyde koruma gerektirir. Bu proje ile:

- **Sağlık veri sistemleri analiz edilir**
- **HIPAA gibi regülasyonlara uyum durumu değerlendirilir**
- **Gizlilik riskleri ve veri ifşa potansiyelleri tespit edilir**
- **LLM kullanarak risk azaltma stratejileri önerilir**

---

## 🔍 İncelenen Regülasyonlar

- **PII (Personally Identifiable Information)**
- **HIPAA (Health Insurance Portability and Accountability Act)**
- **GDPR (General Data Protection Regulation)**
- **KVKK (Kişisel Verilerin Korunması Kanunu – Türkiye)**
- **PCI DSS (Payment Card Industry Data Security Standard)**

---

## 🚀 Özellikler

- 🧠 LLM (LLaMA3) destekli analiz
- 📊 Yüklenen CSV veri setinin otomatik değerlendirilmesi
- ❌ Riskli sütunların otomatik tespiti ve çıkarılması
- 📁 Temizlenmiş veri setinin indirilmesi
- 📋 Her sütun için açıklamalı regülasyon ihlali raporu

---

## 🧰 Ek Modüller

- **Eğitim Materyalleri**: Personelin sağlık veri mahremiyeti konusunda eğitilmesi için kullanılabilecek içerikler sunar.
- **Politika Şablonları**: Kurumlar için veri koruma politikalarının hazırlanmasında kullanılabilecek öneri dokümanları.

---

## 💻 Kullanım

1. Uygulamayı başlatın:
    ```bash
    streamlit run app.py
    ```

2. CSV formatında bir sağlık veri seti yükleyin.
3. “LLM ile Analizi Başlat” butonuna tıklayın.
4. LLM değerlendirmesine göre oluşturulan temiz veri setini indirin.

---

## 📎 Katkıda Bulun

Katkılar her zaman memnuniyetle karşılanır! Fork’layabilir, geliştirme yapabilir ve pull request gönderebilirsiniz.

---

## ©️ Lisans

Bu proje [MIT License](LICENSE) ile lisanslanmıştır.
