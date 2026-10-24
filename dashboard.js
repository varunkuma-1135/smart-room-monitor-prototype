let chart;

function prettyRoom(name) {
  return name.replaceAll("-", " ").replace(/\b\w/g, letter => letter.toUpperCase());
}

async function getJSON(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Request failed: ${url}`);
  return response.json();
}

function renderRooms(readings) {
  const container = document.getElementById("rooms");
  if (!readings.length) {
    container.innerHTML = '<div class="empty">No readings yet. Start the sensor simulator in another terminal.</div>';
    return;
  }
  container.innerHTML = readings.map(item => {
    const isAlert = item.status !== "NORMAL";
    const statusText = item.status === "HIGH_TEMP" ? "HIGH TEMPERATURE"
      : item.status === "HIGH_HUMIDITY" ? "HIGH HUMIDITY" : "NORMAL";
    return `<article class="room-card ${isAlert ? "alert" : ""}">
      <div class="room-title"><span>${prettyRoom(item.device_id)}</span><span class="status">${statusText}</span></div>
      <div class="reading">${Number(item.temperature).toFixed(1)}°C</div>
      <div class="humidity">Humidity: ${Number(item.humidity).toFixed(1)}%</div>
    </article>`;
  }).join("");
}

function renderChart(readings) {
  const roomNames = [...new Set(readings.map(item => item.device_id))];
  const palette = ["#2767b1", "#1f9b70", "#e49a38", "#8657c7"];
  const labels = readings.map((_, index) => index + 1);
  const datasets = roomNames.map((room, index) => ({
    label: prettyRoom(room),
    data: readings.map(item => item.device_id === room ? item.temperature : null),
    borderColor: palette[index % palette.length],
    backgroundColor: palette[index % palette.length],
    spanGaps: false,
    tension: 0.25,
    pointRadius: 2
  }));
  datasets.push({
    label: "Alert limit (35°C)",
    data: readings.map(() => 35),
    borderColor: "#dc4c55",
    borderDash: [6, 5],
    pointRadius: 0,
    borderWidth: 2
  });

  if (chart) chart.destroy();
  chart = new Chart(document.getElementById("temperatureChart"), {
    type: "line",
    data: { labels, datasets },
    options: {
      responsive: true, maintainAspectRatio: false,
      interaction: { intersect: false, mode: "index" },
      scales: { y: { title: { display: true, text: "Temperature (°C)" } },
                x: { title: { display: true, text: "Recent readings" } } },
      plugins: { legend: { position: "bottom" } }
    }
  });
}

async function refreshDashboard() {
  try {
    const [latest, history, stats] = await Promise.all([
      getJSON("/api/latest"), getJSON("/api/history?limit=45"), getJSON("/api/stats")
    ]);
    renderRooms(latest);
    renderChart(history);
    document.getElementById("total").textContent = stats.total;
    document.getElementById("avgTemp").textContent = `${stats.avg_temp} °C`;
    document.getElementById("avgHumidity").textContent = `${stats.avg_humidity} %`;
    document.getElementById("alerts").textContent = stats.alerts;
    document.getElementById("updated").textContent = `Last updated: ${new Date().toLocaleTimeString()}`;
  } catch (error) {
    document.getElementById("updated").textContent = "Could not connect to API. Check that app.py is running.";
    console.error(error);
  }
}

document.getElementById("refreshBtn").addEventListener("click", refreshDashboard);
refreshDashboard();
setInterval(refreshDashboard, 3000);
