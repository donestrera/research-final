// WebSocket connection
let socket = null;
let isConnected = false;
const connectionStatus = document.getElementById('connection-status');

// Initialize WebSocket connection
function connectWebSocket() {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws/sensors/`;
    
    socket = new WebSocket(wsUrl);
    
    socket.onopen = () => {
        isConnected = true;
        updateConnectionStatus();
    };
    
    socket.onclose = () => {
        isConnected = false;
        updateConnectionStatus();
        // Attempt to reconnect after 5 seconds
        setTimeout(connectWebSocket, 5000);
    };
    
    socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        isConnected = false;
        updateConnectionStatus();
    };
    
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        updateDashboard(data);
    };
}

// Update connection status display
function updateConnectionStatus() {
    const statusText = isConnected ? 'Connected' : 'Disconnected';
    const statusClass = isConnected ? 'connected' : 'disconnected';
    connectionStatus.innerHTML = `Status: <span class="${statusClass}">${statusText}</span>`;
}

// Update dashboard with new sensor data
function updateDashboard(data) {
    // Update temperature
    const tempValue = document.getElementById('temperature-value');
    if (tempValue) {
        tempValue.textContent = data.temperature.toFixed(1);
    }
    
    // Update humidity
    const humidityValue = document.getElementById('humidity-value');
    if (humidityValue) {
        humidityValue.textContent = data.humidity.toFixed(1);
    }
    
    // Update motion detection
    const motionCard = document.getElementById('motion-card');
    if (motionCard) {
        motionCard.classList.toggle('active', data.motion_detected);
        const motionStatus = motionCard.querySelector('.sensor-status');
        if (motionStatus) {
            motionStatus.textContent = data.motion_detected ? 'Motion Detected' : 'No Motion';
        }
    }
    
    // Update smoke detection
    const smokeCard = document.getElementById('smoke-card');
    if (smokeCard) {
        smokeCard.classList.toggle('active', data.smoke_detected);
        const smokeStatus = smokeCard.querySelector('.sensor-status');
        if (smokeStatus) {
            smokeStatus.textContent = data.smoke_detected ? 'Smoke Detected' : 'No Smoke';
        }
    }
    
    // Add new reading to the table
    addReadingToTable(data);
}

// Add a new reading to the readings table
function addReadingToTable(data) {
    const tbody = document.querySelector('.readings-table tbody');
    if (!tbody) return;
    
    const row = document.createElement('tr');
    const timestamp = new Date().toLocaleTimeString();
    
    row.innerHTML = `
        <td>${timestamp}</td>
        <td>${data.temperature.toFixed(1)}°C</td>
        <td>${data.humidity.toFixed(1)}%</td>
        <td>${data.motion_detected ? 'Yes' : 'No'}</td>
        <td>${data.smoke_detected ? 'Yes' : 'No'}</td>
    `;
    
    // Insert new row at the beginning of the table
    tbody.insertBefore(row, tbody.firstChild);
    
    // Keep only the last 10 readings
    while (tbody.children.length > 10) {
        tbody.removeChild(tbody.lastChild);
    }
}

// Initialize the dashboard when the page loads
document.addEventListener('DOMContentLoaded', () => {
    connectWebSocket();
}); 