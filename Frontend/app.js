// Initialize map
const map = L.map('map').setView([20.5937, 78.9629], 5); // Centered on India

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Create a marker (initial position)
let marker = L.marker([17.3850, 78.4867]).addTo(map)
  .bindPopup("Tracking Location")
  .openPopup();

// Connect to WebSocket (replace with your backend URL)
const socket = new WebSocket("ws://localhost:8000/ws");

socket.onopen = () => {
  console.log("Connected to WebSocket server");
};

socket.onmessage = (event) => {
  try {
    // Expecting JSON data like: { "lat": 17.4, "lng": 78.5 }
    const data = JSON.parse(event.data);

    if (data.lat && data.lng) {
      // Update marker position
      marker.setLatLng([data.lat, data.lng]);
      map.setView([data.lat, data.lng], 12); // optional: recenter map
    }
  } catch (err) {
    console.error("Invalid data received:", event.data);
  }
};

socket.onclose = () => {
  console.log("WebSocket connection closed");
};
