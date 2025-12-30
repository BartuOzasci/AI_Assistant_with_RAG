function addBubble(text, sender) {
  const chatWindow = document.getElementById("chat-window");
  const bubble = document.createElement("div");
  bubble.className = "bubble " + sender;
  bubble.textContent = text;
  chatWindow.appendChild(bubble);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function addTypingIndicator() {
  const chatWindow = document.getElementById("chat-window");
  const typing = document.createElement("div");
  typing.className = "typing-indicator";
  typing.textContent = "Yanıt hazırlanıyor, lütfen bekleyin...";
  typing.id = "typing-indicator";
  chatWindow.appendChild(typing);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function removeTypingIndicator() {
  const typing = document.getElementById("typing-indicator");
  if (typing) typing.remove();
}

function typeBotAnswer(answer) {
  removeTypingIndicator();
  const chatWindow = document.getElementById("chat-window");
  const bubble = document.createElement("div");
  bubble.className = "bubble bot";
  chatWindow.appendChild(bubble);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  let i = 0;
  function typeChar() {
    if (i <= answer.length) {
      bubble.textContent = answer.slice(0, i);
      i++;
      chatWindow.scrollTop = chatWindow.scrollHeight;
      setTimeout(typeChar, 12);
    }
  }
  typeChar();
}
