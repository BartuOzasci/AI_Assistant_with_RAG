from flask import Flask, request, jsonify, render_template
import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import google.genai as genai

# Çevresel değişkenleri yükle (.env)
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

# Kaynakları başta yükle
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
faiss_index = faiss.read_index("./data/contrat_index.faiss")
with open('data/chunks.pkl', 'rb') as f:
    text_chunks = pickle.load(f)

def configure_gemini():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Lütfen .env dosyasına 'GOOGLE_API_KEY' ekleyin.")
    client = genai.Client(api_key=api_key)
    return client

client = configure_gemini()

# Soruya bağlam bulma fonksiyonu

def get_context(query, embed_model, index, chunks, k=5):
    query_vector = embed_model.encode([query])
    distances, indices = index.search(np.array(query_vector, dtype='float32'), k)
    relevant_texts = [chunks[i] for i in indices[0] if i < len(chunks)]
    return "\n---\n".join(relevant_texts)

@app.route('/')
def home():
    # CSS ve JS dosyaları static/css ve static/js altından otomatik sunulur
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form.get('question', '')
    pdf_file = request.files.get('pdf')
    if not question:
        return jsonify({'answer': 'Soru boş olamaz.'})
    # PDF dosyası yüklendiyse burada işlenebilir (örneğin metin çıkarma)
    pdf_text = ''
    if pdf_file:
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                pdf_text += page.extract_text() or ''
        except Exception as e:
            return jsonify({'answer': f'PDF okunamadı: {str(e)}'})
    try:
        context = get_context(question, embedding_model, faiss_index, text_chunks)
        # PDF'den metin varsa bağlama ekle
        if pdf_text:
            context = pdf_text + "\n---\n" + context
        prompt = (
            f"Aşağıdaki bağlam bilgisini kullanarak soruyu cevapla. "
            f"Eğer bağlamda bilgi yoksa, 'Bilgi dokümanlarda bulunamadı' de.\n\n"
            f"BAĞLAM:\n{context}\n\n"
            f"SORU: {question}\n\n"
            f"CEVAP:"
        )
        response = client.models.generate_content(model="models/gemini-2.5-flash", contents=prompt)
        return jsonify({'answer': response.text})
    except Exception as e:
        return jsonify({'answer': f'Hata: {str(e)}'})

if __name__ == "__main__":
    app.run(debug=True)
