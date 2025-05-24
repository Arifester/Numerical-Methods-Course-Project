document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");

  // Validasi fungsi mengandung 'x'
  if (form) {
    form.addEventListener("submit", (e) => {
      const fx = form.querySelector('input[name="function"]').value.trim();
      const x0 = form.querySelector('#x0').value;
      const x1 = form.querySelector('#x1').value;

      if (!fx.includes("x")) {
        e.preventDefault();
        alert("Fungsi harus mengandung variabel 'x'. Contoh: x**2 - 4");
      }
      if ( x0 == x1) {
        e.preventDefault();
        alert("Nilai x0 dan x1 tidak boleh sama.");
      }

      
    });
  }

});
