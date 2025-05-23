document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');

  // Validasi fungsi mengandung 'x'
  if (form) {
    form.addEventListener('submit', (e) => {
      const fx = form.querySelector('input[name="function"]').value.trim();
      if (!fx.includes('x')) {
        e.preventDefault();
        alert("Fungsi harus mengandung variabel 'x'. Contoh: x**2 - 4");
      }
    });
  }

  // Tampilkan grafik jika data tersedia
  if (window.iterations && window.xValues && window.errors) {
    const ctx = document.getElementById('secantChart').getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: window.iterations,
        datasets: [
          {
            label: 'x per Iterasi',
            data: window.xValues,
            borderColor: '#3b82f6',
            fill: false,
            tension: 0.3
          },
          {
            label: 'Error per Iterasi',
            data: window.errors,
            borderColor: '#f87171',
            fill: false,
            tension: 0.3
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Grafik Konvergensi Metode Secant'
          }
        }
      }
    });
  }
});
