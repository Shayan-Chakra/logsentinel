from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from logsentinel.database import get_alerts

app = FastAPI(title="LogSentinel Dashboard")

PAGE = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>LogSentinel Dashboard</title>
<style>
  body { font-family: Arial; margin: 40px; background: #f5f5f5; }
  .cards { display: flex; gap: 20px; margin-bottom: 30px; }
  .card { background: white; padding: 20px 30px; border-radius: 8px; }
  .card h2 { margin: 0; font-size: 36px; }
  .card p { margin: 5px 0 0; color: #666; }
  table { border-collapse: collapse; width: 100%; background: white; }
  th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
  th { background: #333; color: white; }
</style>
</head>
<body>
<h1>LogSentinel Dashboard</h1>
<div class="cards">
  <div class="card"><h2 id="total">0</h2><p>Total alerts</p></div>
  <div class="card"><h2 id="critical">0</h2><p>Break-ins (critical)</p></div>
</div>
<table>
  <thead>
    <tr><th>Time</th><th>Rule</th><th>IP</th><th>User</th><th>Count</th></tr>
  </thead>
  <tbody id="rows"></tbody>
</table>
<script>
async function load() {
  const res = await fetch("/api/alerts");
  const alerts = await res.json();

  document.getElementById("total").textContent = alerts.length;
  document.getElementById("critical").textContent =
    alerts.filter(a => a.rule === "SUCCESS_AFTER_FAILURE").length;

  const body = document.getElementById("rows");
  body.innerHTML = "";
  for (const a of alerts) {
    const tr = document.createElement("tr");
    const values = [a.created_at, a.rule, a.ip, a.username, a.count ?? a.failures];
    for (const v of values) {
      const td = document.createElement("td");
      td.textContent = v ?? "-";
      tr.appendChild(td);
    }
    body.appendChild(tr);
  }
}
load();
setInterval(load, 5000);
</script>
</body>
</html>"""


@app.get("/api/alerts")
def alerts():
    return get_alerts(200)


@app.get("/", response_class=HTMLResponse)
def dashboard():
    return PAGE