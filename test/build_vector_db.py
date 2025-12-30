
# Gerekli kütüphaneler içe aktarılıyor
import os
import fitz  # PyMuPDF kütüphanesi
from sentence_transformers import SentenceTransformer  # Cümle gömme modeli
import faiss  # Vektör veritabanı için
import numpy as np  # Sayısal işlemler için
import pickle  # Nesne serileştirme için



# PDF dosyalarından metin çıkaran fonksiyon
def extract_text_from_pdfs(pdf_folder):
    texts = []
    for filename in os.listdir(pdf_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, filename)
            with fitz.open(pdf_path) as doc:
                for page in doc:
                    texts.append(page.get_text())  # Her sayfanın metni ekleniyor
    return texts

# tek dosya için ve çift dosya için
'''
# PDF dosyalarından metin çıkaran fonksiyon
def extract_text_from_pdfs(pdf_folder):
    doc = fitz.open(pdf_folder)
    text = ""
    for page in doc:
        text += page.get_text()

    return text
'''

# Metni parçalara bölen fonksiyon
def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

model = SentenceTransformer('all-MiniLM-L6-v2')  # Cümle gömme modeli yükleniyor

pdf_files_path = './data'


# PDF dosyalarından çıkan metinler birleştiriliyor
text = " ".join(extract_text_from_pdfs(pdf_files_path))

# Metin parçalara bölünüyor
chunks = chunk_text(text, chunk_size=500, overlap=50)

embeddings = model.encode(chunks)  # Parçalar gömülüyor




dimension = embeddings.shape[1]  # Gömme boyutu
index = faiss.IndexFlatL2(dimension)  # FAISS indeksi oluşturuluyor
index.add(np.array(embeddings, dtype='float32'))  # Gömme indekse ekleniyor

faiss.write_index(index, 'data/contrat_index.faiss')  # İndeks diske kaydediliyor
with open('data/chunks.pkl', 'wb') as f:
    pickle.dump(chunks, f)  # Parçalar diske kaydediliyor

print("Vektör veritabanı başarıyla oluşturuldu ve kaydedildi.")