// When served by FastAPI (port 8000) use a relative URL; otherwise (Live Server, file://) call the backend directly.
const API_BASE = location.port === "8000" ? "/api" : "http://localhost:8000/api";
const POLL_MS = 2000;

const map = L.map("map").setView([12.9755, 77.5900], 14);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "&copy; OpenStreetMap contributors",
  maxZoom: 19,
}).addTo(map);

const routeLayer = L.layerGroup().addTo(map);
const vehicleMarkers = {}; // vehicle id -> L.marker
let routes = [];
let routeColors = {};

const $ = (id) => document.getElementById(id);

function esc(text) {
  const d = document.createElement("div");
  d.textContent = text ?? "";
  return d.innerHTML;
}

async function api(path) {
  const res = await fetch(API_BASE + path);
  if (!res.ok) throw new Error(`${path} -> ${res.status}`);
  return res.json();
}

function setConnection(ok) {
  const el = $("conn");
  el.textContent = ok ? "Live" : "Backend offline";
  el.className = "text-sm px-2 py-1 rounded " + (ok ? "bg-green-500" : "bg-red-500");
}

// ---- Routes & stops (loaded once) ----
async function loadRoutes() {
  routes = await api("/routes");
  routeColors = Object.fromEntries(routes.map((r) => [r.id, r.color]));
  routeLayer.clearLayers();

  const bounds = [];
  routes.forEach((route) => {
    const pts = route.stops.map((s) => [s.latitude, s.longitude]);
    bounds.push(...pts);
    if (pts.length > 1) {
      L.polyline([...pts, pts[0]], { color: route.color, weight: 4, opacity: 0.6 }).addTo(routeLayer);
    }
    route.stops.forEach((s) => {
      L.circleMarker([s.latitude, s.longitude], {
        radius: 6, color: route.color, fillColor: "#fff", fillOpacity: 1, weight: 3,
      }).bindTooltip(esc(s.name)).addTo(routeLayer);
    });
  });
  if (bounds.length) map.fitBounds(bounds, { padding: [40, 40] });

  $("route-list").innerHTML = routes
    .map((r) => `<li class="flex items-center gap-2">
        <span class="inline-block w-3 h-3 rounded-full" style="background:${esc(r.color)}"></span>
        ${esc(r.name)} <span class="text-gray-400">(${r.stops.length} stops)</span></li>`)
    .join("");
}

// ---- Vehicles (polled) ----
function busIcon(vehicle) {
  const color = routeColors[vehicle.route_id] || "#2563eb";
  return L.divIcon({
    className: "",
    html: `<div class="bus-marker ${esc(vehicle.status)}" style="background:${esc(color)}"></div>`,
    iconSize: [18, 18],
    iconAnchor: [9, 9],
  });
}

function popupHtml(v) {
  const route = routes.find((r) => r.id === v.route_id);
  const stop = route?.stops.find((s) => s.id === v.current_stop_id);
  return `<b>${esc(v.name)}</b><br>Route: ${esc(route?.name ?? v.route_id)}<br>` +
         `Status: ${esc(v.status)}` + (stop ? `<br>Near: ${esc(stop.name)}` : "");
}

function renderVehicles(vehicles) {
  const seen = new Set();

  vehicles.forEach((v) => {
    if (v.latitude == null || v.longitude == null) return;
    seen.add(v.id);
    const pos = [v.latitude, v.longitude];
    let marker = vehicleMarkers[v.id];
    if (!marker) {
      marker = vehicleMarkers[v.id] = L.marker(pos, { icon: busIcon(v) }).addTo(map);
      marker.bindPopup(popupHtml(v));
    } else {
      marker.setLatLng(pos);
      marker.setIcon(busIcon(v));
      marker.setPopupContent(popupHtml(v));
    }
  });

  // remove markers for deleted vehicles
  Object.keys(vehicleMarkers).forEach((id) => {
    if (!seen.has(id)) {
      map.removeLayer(vehicleMarkers[id]);
      delete vehicleMarkers[id];
    }
  });

  const badge = { moving: "text-green-600", delayed: "text-amber-600", idle: "text-gray-500" };
  $("vehicle-list").innerHTML = vehicles
    .map((v) => `<li><button data-id="${esc(v.id)}" class="w-full text-left hover:bg-gray-100 rounded px-1 py-1">
        ${esc(v.name)} <span class="${badge[v.status] || ""} float-right">${esc(v.status)}</span></button></li>`)
    .join("");
}

$("vehicle-list").addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-id]");
  const marker = btn && vehicleMarkers[btn.dataset.id];
  if (marker) {
    map.flyTo(marker.getLatLng(), 16);
    marker.openPopup();
  }
});

async function pollVehicles() {
  try {
    if (!routes.length) await loadRoutes(); // retry if backend came up late
    renderVehicles(await api("/vehicles"));
    setConnection(true);
  } catch (err) {
    console.error(err);
    setConnection(false);
  }
}

pollVehicles();
setInterval(pollVehicles, POLL_MS);
