const API_BASE = "http://127.0.0.1:8000";
const form = document.getElementById("analyzeForm");
const input = document.getElementById("urlInput");
const button = document.getElementById("analyzeBtn");
const statusText = document.getElementById("status");
const results = document.getElementById("results");
const serviceStatus = document.getElementById("serviceStatus");
const serviceStatusMessage = document.getElementById("serviceStatusMessage");

form.addEventListener("submit", async event => { event.preventDefault(); await analyzeUrl(); });
document.getElementById("refreshStatus").addEventListener("click", loadServiceStatus);

async function loadServiceStatus() {
  serviceStatusMessage.textContent = "Checking backend…";
  try {
    const response = await fetch(`${API_BASE}/api/health`);
    if (!response.ok) throw new Error("Backend returned an error.");
    const data = await response.json();
    serviceStatus.replaceChildren();
    data.services.forEach(service => {
      const card = document.createElement("div");
      card.className = "service-card";
      const dot = document.createElement("span"); dot.className = "status-dot online";
      const name = document.createElement("strong"); name.textContent = service.name;
      const state = document.createElement("small"); state.textContent = service.status === "running" ? "Available" : service.status;
      card.append(dot, name, state); serviceStatus.appendChild(card);
    });
    serviceStatusMessage.textContent = "Backend connected. The services are ready to receive requests.";
  } catch (error) {
    serviceStatusMessage.textContent = "Could not reach the backend. Make sure it is running on port 8000.";
    serviceStatus.querySelectorAll(".status-dot").forEach(dot => dot.className = "status-dot offline");
  }
}

async function analyzeUrl() {
  const url = input.value.trim();
  if (!url) { statusText.textContent = "Please enter a URL."; return; }
  button.disabled = true; statusText.textContent = "Sending URL to the services…"; results.classList.add("hidden");
  try {
    const response = await fetch(`${API_BASE}/api/analyze`, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({url})});
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "The URL could not be analyzed.");
    document.getElementById("prediction").textContent = data.prediction;
    document.getElementById("checkedUrl").textContent = data.url;
    const badge = document.getElementById("riskBadge");
    badge.textContent = `${data.risk_level} risk`; badge.className = `risk-badge ${data.risk_level.toLowerCase()}`;
    document.getElementById("score").textContent = `${data.risk_score}/100`;
    document.getElementById("meterFill").style.width = `${data.risk_score}%`;
    const list = document.getElementById("reasons"); list.replaceChildren();
    data.reasons.forEach(reason => { const li = document.createElement("li"); li.textContent = reason; list.appendChild(li); });
    document.getElementById("riskSummary").textContent = `The service rated this URL ${data.risk_level.toLowerCase()} risk, with a score of ${data.risk_score}/100.`;
    document.getElementById("action").textContent = data.response.action.replaceAll("_", " ");
    document.getElementById("responseMessage").textContent = data.response.message;
    document.getElementById("simulated").textContent = "Prototype only: no actual network blocking or external reporting is performed.";
    document.getElementById("note").textContent = data.note;
    results.classList.remove("hidden"); statusText.textContent = "Analysis complete. All three services returned results.";
  } catch (error) { statusText.textContent = `${error.message} Check that the backend is running.`; }
  finally { button.disabled = false; }
}
loadServiceStatus();
