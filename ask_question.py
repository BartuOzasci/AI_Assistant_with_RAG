import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import google.generativeai as genai

# Çevresel değişkenleri yükle (.env)
load_dotenv()

def configure_gemini():
    """
    Google Gemini API'sini yapılandırır ve en verimli modeli seçer.
    
    Seçilen Model: models/gemini-2.5-flash
    Neden: Hız (Flash mimarisi) ve performans (v2.5) dengesi en yüksek modeldir.
    
    Returns:
        genai.GenerativeModel: Yapılandırılmış model nesnesi.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Lütfen .env dosyasına 'GOOGLE_API_KEY' ekleyin.")

    genai.configure(api_key=api_key)
    
    # Listeden seçilen en performanslı ve hızlı model
    model_name = "models/gemini-2.5-flash"
    
    try:
        model = genai.GenerativeModel(model_name)
        return model
    except Exception as e:
        print(f"Model yüklenirken hata oluştu: {e}")
        print("Yedek model (gemini-2.0-flash) deneniyor...")
        return genai.GenerativeModel("models/gemini-2.0-flash")

def load_rag_resources():
    """
    Vektör veritabanı, embedding modeli ve metin parçalarını hafızaya yükler.
    Bu işlem maliyetli olduğu için program başında sadece bir kez yapılır.
    
    Returns:
        tuple: (embedding_model, faiss_index, text_chunks)
    """
    print("Sistem kaynakları yükleniyor, lütfen bekleyin...")
    
    # 1. Embedding Modelini Yükle
    # 'all-MiniLM-L6-v2': Hızlı ve RAG için yeterli bir embedding modelidir.
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 2. FAISS İndeksini Yükle
    try:
        faiss_index = faiss.read_index("./data/contrat_index.faiss")
    except Exception as e:
        print(f"Kritik Hata: FAISS indeksi okunamadı. ({e})")
        exit(1)

    # 3. Metin Parçalarını (Chunks) Yükle
    try:
        with open('data/chunks.pkl', 'rb') as f:
            text_chunks = pickle.load(f)
    except Exception as e:
        print(f"Kritik Hata: Chunks dosyası okunamadı. ({e})")
        exit(1)
        
    print("Kaynaklar başarıyla yüklendi.\n")
    return embedding_model, faiss_index, text_chunks

def get_context(query, embed_model, index, chunks, k=5):
    """
    Kullanıcı sorusuna en benzer metin parçalarını getirir.
    
    Args:
        query (str): Kullanıcı sorusu.
        embed_model: SentenceTransformer modeli.
        index: FAISS indeksi.
        chunks: Metin listesi.
        k (int): Getirilecek parça sayısı.
        
    Returns:
        str: Birleştirilmiş bağlam metni.
    """
    # Soruyu vektöre çevir
    query_vector = embed_model.encode([query])
    
    # FAISS araması (float32 tip zorunluluğu vardır)
    distances, indices = index.search(np.array(query_vector, dtype='float32'), k)
    
    # İndekslerden metinleri çek ve birleştir
    # indices[0] olmasının sebebi search fonksiyonunun 2D dizi döndürmesidir
    relevant_texts = [chunks[i] for i in indices[0] if i < len(chunks)]
    
    return "\n---\n".join(relevant_texts)

def main():
    """
    Ana çalışma döngüsü.
    """
    # Kaynakları yükle
    embed_model, vector_index, data_chunks = load_rag_resources()
    
    # Gemini modelini hazırla
    llm = configure_gemini()
    
    print("Asistan Hazır. (Çıkış için 'q', 'exit' yazabilirsiniz)")
    print("-" * 50)

    while True:
        query = input("Soru: ").strip()
        
        # Çıkış kontrolü
        if query.lower() in ['exit', 'quit', 'çıkış', 'q']:
            print("Çıkılıyor...")
            break
            
        if not query:
            continue

        try:
            # İlgili bağlamı bul
            context = get_context(query, embed_model, vector_index, data_chunks)
            
            # LLM için prompt hazırla
            # Prompt, modelin sadece verilen bilgiyi kullanmasını sağlar
            prompt = (
                f"Aşağıdaki bağlam bilgisini kullanarak soruyu cevapla. "
                f"Eğer bağlamda bilgi yoksa, 'Bilgi dokümanlarda bulunamadı' de.\n\n"
                f"BAĞLAM:\n{context}\n\n"
                f"SORU: {query}\n\n"
                f"CEVAP:"
            )
            
            # Gemini'ye gönder
            response = llm.generate_content(prompt)
            
            # Cevabı yazdır
            print(f"\nCevap:\n{response.text}")
            print("-" * 50)
            
        except Exception as e:
            print(f"İşlem sırasında bir hata oluştu: {e}")

if __name__ == "__main__":
    main()