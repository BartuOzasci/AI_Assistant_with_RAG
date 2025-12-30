document
  .getElementById("questionForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();
    const textarea = document.getElementById("question");
    const pdfInput = document.getElementById("pdf");
    const question = textarea.value.trim();
    if (!question) return;
    addBubble(question, "user");
    textarea.value = "";
    addTypingIndicator();
    const pdfFile = pdfInput.files[0];
    const formData = new FormData();
    formData.append("question", question);
    if (pdfFile) formData.append("pdf", pdfFile);
    try {
      const res = await fetch("/ask", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      typeBotAnswer(data.answer || "Yanıt alınamadı.");
    } catch {
      removeTypingIndicator();
      typeBotAnswer("Bir hata oluştu.");
    }
    // pdfInput.value ve pdfNameSpan temizlenmiyor, dosya seçili kalıyor
  });

document.getElementById("question").addEventListener("keydown", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    document
      .getElementById("questionForm")
      .dispatchEvent(new Event("submit", { cancelable: true, bubbles: true }));
  }
});
