document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");

  // Validasi fungsi mengandung 'x'
  if (form) {
    form.addEventListener("submit", (e) => {
      const fx = form.querySelector('input[name="function"]').value.trim();
      if (!fx.includes("x")) {
        e.preventDefault();
        alert("Fungsi harus mengandung variabel 'x'. Contoh: x**2 - 4");
      }
    });
  }

  // Tampilkan grafik jika data tersedia
  if (window.iterations && window.xValues && window.errors) {
    const ctx = document.getElementById("resultChart").getContext("2d");
    new Chart(ctx, {
      type: "line",
      data: {
        labels: window.iterations,
        datasets: [
          {
            label: "Nilai x per Iterasi",
            data: window.xValues,
            borderColor: "#3b82f6", // Warna biru
            fill: false,
            tension: 0.3,
          },
          {
            label: "Error per Iterasi",
            data: window.errors,
            borderColor: "#f87171", // Warna merah
            fill: false,
            tension: 0.3,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: "Grafik Konvergensi Metode Secant",
          },
          tooltip: {
            callbacks: {
              label: function (tooltipItem) {
                return `${tooltipItem.dataset.label}: ${tooltipItem.raw.toFixed(
                  6
                )}`;
              },
            },
          },
        },
        scales: {
          x: {
            title: {
              display: true,
              text: "Iterasi",
            },
          },
          y: {
            title: {
              display: true,
              text: "Nilai",
            },
            beginAtZero: false,
          },
        },
      },
    });
  } else {
    console.warn("Data untuk grafik tidak tersedia.");
  }
});
