document.getElementById("pdf").addEventListener("change", function () {
  const pdfInput = document.getElementById("pdf");
  const pdfNameSpan = document.getElementById("pdf-name");
  if (pdfInput.files.length > 0) {
    const fileName = pdfInput.files[0].name;
    pdfNameSpan.innerHTML = `${fileName} <span class='pdf-remove' title='Kaldır'>×</span>`;
    document.querySelector(".pdf-remove").onclick = function () {
      pdfInput.value = "";
      pdfNameSpan.textContent = "";
    };
  } else {
    pdfNameSpan.textContent = "";
  }
});
