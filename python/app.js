/* Crystal — Resistivity Scanner | app.js */

let chart = null;
let polling = null;

function startScan() {
  fetch('/start')
    .then(r => {
      if (r.ok) {
        document.getElementById('scan-btn').disabled = true;
        document.getElementById('download-btn').style.display = 'none';
        document.getElementById('error-box').style.display = 'none';
        polling = setInterval(pollStatus, 500);
      }
    })
    .catch(() => showError('Could not connect to scanner. Is main.py running?'));
}

function pollStatus() {
  fetch('/status')
    .then(r => r.json())
    .then(state => {
      updateUI(state);
      if (state.status === 'complete' || state.status === 'error') {
        clearInterval(polling);
        document.getElementById('scan-btn').disabled = false;
        if (state.status === 'complete') document.getElementById('download-btn').style.display = 'inline-block';
        if (state.status === 'error') showError(state.error || 'Unknown error');
      }
    })
    .catch(() => clearInterval(polling));
}

function updateUI(state) {
  const statusEl = document.getElementById('status-text');
  const bar = document.getElementById('progress-bar');
  bar.style.width = state.progress + '%';

  if (state.status === 'scanning') {
    statusEl.style.color = '#d97706';
    statusEl.textContent = `Scanning… ${state.progress}% (${state.current_position} mm)`;
  } else if (state.status === 'complete') {
    statusEl.style.color = '#16a34a';
    statusEl.textContent = 'Scan complete';
  } else if (state.status === 'error') {
    statusEl.style.color = '#dc2626';
    statusEl.textContent = 'Error';
  }

  const results = state.results || [];
  if (results.length === 0) return;

  if (state.status === 'complete') document.getElementById('demo-label').style.display = '';

  const resistances = results.map(r => r.resistance);
  const avg = (resistances.reduce((a, b) => a + b, 0) / resistances.length).toFixed(1);
  const min = Math.min(...resistances).toFixed(1);
  const max = Math.max(...resistances).toFixed(1);

  document.getElementById('avg').innerHTML = `${avg} <span class="summary-unit">Ω/□</span>`;
  document.getElementById('min').textContent = `${min} Ω/□`;
  document.getElementById('max').textContent = `${max} Ω/□`;

  document.getElementById('chart-empty').style.display = 'none';
  const labels = results.map(r => r.position + ' mm');
  const data = results.map(r => r.resistance);

  if (!chart) {
    const ctx = document.getElementById('chart').getContext('2d');
    chart = new Chart(ctx, {
      type: 'line',
      data: { labels, datasets: [{ label: 'Sheet resistance (Ω/□)', data, borderColor: '#1d4ed8', backgroundColor: 'rgba(29,78,216,0.07)', borderWidth: 2, pointRadius: results.length > 50 ? 0 : 3, tension: 0.3, fill: true }] },
      options: { responsive: true, animation: false, plugins: { legend: { display: false } }, scales: { x: { title: { display: true, text: 'Position (mm)', font: { size: 11 } }, ticks: { maxTicksLimit: 12, font: { size: 11 } } }, y: { title: { display: true, text: 'Ω/□', font: { size: 11 } }, ticks: { font: { size: 11 } } } } }
    });
  } else {
    chart.data.labels = labels;
    chart.data.datasets[0].data = data;
    chart.update();
  }

  const recent = results.slice(-20).reverse();
  let html = `<table><thead><tr><th>Position (mm)</th><th>Voltage (V)</th><th>Rs (Ω/□)</th><th>Time</th><th>Status</th></tr></thead><tbody>`;
  recent.forEach(r => { html += `<tr><td>${r.position} mm</td><td>${r.voltage}</td><td>${r.resistance}</td><td>${r.timestamp}</td><td><span class="badge-ok">ok</span></td></tr>`; });
  html += '</tbody></table>';
  if (results.length > 20) html += `<p style="font-size:12px;color:#aaa;padding:8px 8px 0">Showing last 20 of ${results.length} readings. Download CSV for full data.</p>`;
  document.getElementById('table-wrap').innerHTML = html;
}

function downloadCSV() { window.location.href = '/download'; }

function showError(msg) {
  const el = document.getElementById('error-box');
  el.textContent = 'Error: ' + msg;
  el.style.display = 'block';
}
