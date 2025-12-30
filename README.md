# RAG Avukat Asistanı

Bu proje, avukatlar ve hukuk profesyonelleri için geliştirilmiş bir Yapay Zeka (AI) destekli sohbet ve belge analiz asistanıdır. Flask tabanlı web arayüzü ile kullanıcıların sorularını yanıtlar, PDF belgeleri yükleyip analiz edebilir ve vektör tabanlı arama ile bilgiye hızlı erişim sağlar.

## Proje Klasör Yapısı

```
RAG_Avukat/
├── app.py                # Ana Flask uygulaması
├── api_modelleri.py      # API modelleri (test klasörüne taşındı)
├── ask_question.py       # Soru-cevap fonksiyonları (test klasörüne taşındı)
├── build_vector_db.py    # Vektör veritabanı oluşturucu (test klasörüne taşındı)
├── requirements.txt      # Gerekli Python paketleri
├── data/                 # Vektör veritabanı ve veri dosyaları
│   └── contrat_index.faiss
├── static/
│   ├── css/              # CSS dosyaları (utils, style, responsive)
│   └── js/               # JS dosyaları (chat, form, pdf)
├── templates/
│   └── index.html        # Ana HTML şablonu
└── test/                 # Test ve yardımcı scriptler (açıklama aşağıda)
```

## test/ Klasörü Nedir?

test/ klasörü, projenin ana işleyişini bozmadan geliştirme, test ve bakım işlemlerini kolaylaştırmak için oluşturulmuştur. Bu klasörde şunlar bulunur:

- **api_modelleri.py**: API ile ilgili model tanımları ve yardımcı fonksiyonlar.
- **ask_question.py**: Soru-cevap ve bilgi getirme fonksiyonlarının bağımsız testleri.
- **build_vector_db.py**: Vektör veritabanı oluşturma ve güncelleme scripti.

Bu dosyalar, ana uygulamadan bağımsız olarak çalıştırılabilir. Böylece yeni özellikler eklerken veya mevcut fonksiyonları test ederken ana uygulamanın stabilitesini koruyabilirsiniz. Ayrıca, vektör veritabanı güncellemeleri veya model testleri için ana uygulamayı başlatmanıza gerek kalmaz.

## Kurulum ve Çalıştırma

1. **Ortamı Hazırlayın:**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Uygulamayı Başlatın:**

   ```bash
   python app.py
   ```

   Ardından tarayıcınızda `http://localhost:5000` adresine gidin.

3. **Vektör Veritabanı Oluşturma (İlk Kurulumda):**
   Eğer veri tabanınız yoksa veya güncellemek isterseniz:
   ```bash
   python test/build_vector_db.py
   ```

## Özellikler

- Modern ve profesyonel web arayüzü
- PDF yükleyip analiz etme
- Gelişmiş sohbet ve soru-cevap
- Vektör tabanlı hızlı arama
- Kolay test ve bakım için ayrı test/ klasörü

## Katkı ve Geliştirme

- Kodlarınızda değişiklik yapmadan önce test/ klasöründe fonksiyonları deneyebilirsiniz.
- Yeni özellik eklerken test scriptleri ile doğrulama yapmanız önerilir.

## Lisans

Bu proje MIT lisansı ile lisanslanmıştır.
