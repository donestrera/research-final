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
        console.log('WebSocket connected');
    };
    
    socket.onclose = () => {
        isConnected = false;
        updateConnectionStatus();
        console.log('WebSocket disconnected, attempting to reconnect...');
        // Attempt to reconnect after 5 seconds
        setTimeout(connectWebSocket, 5000);
    };
    
    socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        isConnected = false;
        updateConnectionStatus();
    };
    
    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            if (data.message) {
                updateDashboard(data.message.data);
            } else {
                updateDashboard(data);
            }
        } catch (error) {
            console.error('Error processing message:', error);
        }
    };
}

// Update connection status display
function updateConnectionStatus() {
    const statusSpan = connectionStatus.querySelector('span');
    statusSpan.textContent = isConnected ? 'Connected' : 'Disconnected';
    statusSpan.className = isConnected ? 'connected' : 'disconnected';
}

// Update dashboard with new sensor data
function updateDashboard(data) {
    if (!data) return;

    // Update temperature
    const tempValue = document.getElementById('temperature-value');
    if (tempValue && data.temperature !== undefined) {
        tempValue.textContent = Number(data.temperature).toFixed(1);
    }
    
    // Update humidity
    const humidityValue = document.getElementById('humidity-value');
    if (humidityValue && data.humidity !== undefined) {
        humidityValue.textContent = Number(data.humidity).toFixed(1);
    }
    
    // Update motion detection
    const motionCard = document.getElementById('motion-card');
    if (motionCard && data.motionDetected !== undefined) {
        motionCard.classList.toggle('active', data.motionDetected);
        const motionStatus = motionCard.querySelector('.sensor-status');
        if (motionStatus) {
            motionStatus.textContent = data.motionDetected ? 'Motion Detected' : 'No Motion';
        }
    }
    
    // Update smoke detection
    const smokeCard = document.getElementById('smoke-card');
    if (smokeCard && data.smokeDetected !== undefined) {
        smokeCard.classList.toggle('active', data.smokeDetected);
        const smokeStatus = smokeCard.querySelector('.sensor-status');
        if (smokeStatus) {
            smokeStatus.textContent = data.smokeDetected ? 'Smoke Detected' : 'No Smoke';
        }
    }
    
    // Add new reading to the table
    addReadingToTable(data);
}

// Add a new reading to the readings table
function addReadingToTable(data) {
    if (!data) return;

    const tbody = document.querySelector('.readings-table tbody');
    if (!tbody) return;
    
    const row = document.createElement('tr');
    const timestamp = new Date().toLocaleTimeString();
    
    row.innerHTML = `
        <td>${timestamp}</td>
        <td>${Number(data.temperature).toFixed(1)}°C</td>
        <td>${Number(data.humidity).toFixed(1)}%</td>
        <td>${data.motionDetected ? 'Yes' : 'No'}</td>
        <td>${data.smokeDetected ? 'Yes' : 'No'}</td>
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
    console.log('Initializing dashboard...');
    connectWebSocket();
}); 