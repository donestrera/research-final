// WebSocket connection
let socket = null;
let isConnected = false;
const connectionStatus = document.getElementById('connection-status');

// Chart objects
let temperatureChart = null;
let humidityChart = null;
let historyTemperatureChart = null;
let historyHumidityChart = null;

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

// Initialize charts
function initializeCharts() {
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        scales: {
            y: {
                beginAtZero: false
            },
            x: {
                type: 'time',
                time: {
                    unit: 'minute'
                }
            }
        }
    };

    // Real-time temperature chart
    const tempCtx = document.getElementById('temperature-chart').getContext('2d');
    temperatureChart = new Chart(tempCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Temperature (°C)',
                data: [],
                borderColor: '#e53e3e',
                tension: 0.4
            }]
        },
        options: commonOptions
    });

    // Real-time humidity chart
    const humCtx = document.getElementById('humidity-chart').getContext('2d');
    humidityChart = new Chart(humCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Humidity (%)',
                data: [],
                borderColor: '#4299e1',
                tension: 0.4
            }]
        },
        options: commonOptions
    });

    // Historical temperature chart
    const histTempCtx = document.getElementById('history-temperature-chart').getContext('2d');
    historyTemperatureChart = new Chart(histTempCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Temperature History (°C)',
                data: [],
                borderColor: '#e53e3e',
                tension: 0.4
            }]
        },
        options: {
            ...commonOptions,
            plugins: {
                title: {
                    display: true,
                    text: 'Temperature History'
                }
            }
        }
    });

    // Historical humidity chart
    const histHumCtx = document.getElementById('history-humidity-chart').getContext('2d');
    historyHumidityChart = new Chart(histHumCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Humidity History (%)',
                data: [],
                borderColor: '#4299e1',
                tension: 0.4
            }]
        },
        options: {
            ...commonOptions,
            plugins: {
                title: {
                    display: true,
                    text: 'Humidity History'
                }
            }
        }
    });
}

// Update dashboard with new sensor data
function updateDashboard(data) {
    if (!data) return;

    const timestamp = new Date();

    // Update temperature
    const tempValue = document.getElementById('temperature-value');
    if (tempValue && data.temperature !== undefined) {
        const temp = Number(data.temperature).toFixed(1);
        tempValue.textContent = temp;
        updateChart(temperatureChart, timestamp, temp);
    }
    
    // Update humidity
    const humidityValue = document.getElementById('humidity-value');
    if (humidityValue && data.humidity !== undefined) {
        const humidity = Number(data.humidity).toFixed(1);
        humidityValue.textContent = humidity;
        updateChart(humidityChart, timestamp, humidity);
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

// Update real-time chart data
function updateChart(chart, label, value) {
    if (!chart) return;

    chart.data.labels.push(label);
    chart.data.datasets[0].data.push(value);

    // Keep only last 60 readings (1 hour at 1 reading per minute)
    if (chart.data.labels.length > 60) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
    }

    chart.update();
}

// Load historical data
async function loadHistoricalData() {
    try {
        const timeRange = document.getElementById('time-range').value;
        const response = await fetch(`/api/historical-data/?hours=${timeRange}`);
        const data = await response.json();

        // Update historical temperature chart
        historyTemperatureChart.data.labels = data.timestamps.map(t => new Date(t));
        historyTemperatureChart.data.datasets[0].data = data.temperature;
        historyTemperatureChart.update();

        // Update historical humidity chart
        historyHumidityChart.data.labels = data.timestamps.map(t => new Date(t));
        historyHumidityChart.data.datasets[0].data = data.humidity;
        historyHumidityChart.update();
    } catch (error) {
        console.error('Error loading historical data:', error);
    }
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
    
    tbody.insertBefore(row, tbody.firstChild);
    
    while (tbody.children.length > 10) {
        tbody.removeChild(tbody.lastChild);
    }
}

// Load security events
async function loadSecurityEvents() {
    try {
        const timeRange = document.getElementById('security-time-range').value;
        const response = await fetch(`/api/security-events/?hours=${timeRange}`);
        const data = await response.json();

        // Update motion events list
        const motionList = document.getElementById('motion-events');
        motionList.innerHTML = '';
        data.motion_events.forEach(event => {
            const eventItem = document.createElement('div');
            eventItem.className = 'event-item';
            eventItem.innerHTML = `
                <div class="event-info">
                    <div class="event-time">${new Date(event.timestamp).toLocaleString()}</div>
                    <div class="event-location">${event.location}</div>
                </div>
                <span class="event-type motion">Motion Detected</span>
            `;
            motionList.appendChild(eventItem);
        });

        // Update smoke events list
        const smokeList = document.getElementById('smoke-events');
        smokeList.innerHTML = '';
        data.smoke_events.forEach(event => {
            const eventItem = document.createElement('div');
            eventItem.className = 'event-item';
            eventItem.innerHTML = `
                <div class="event-info">
                    <div class="event-time">${new Date(event.timestamp).toLocaleString()}</div>
                    <div class="event-location">${event.location}</div>
                </div>
                <span class="event-type smoke">Smoke Detected</span>
            `;
            smokeList.appendChild(eventItem);
        });
    } catch (error) {
        console.error('Error loading security events:', error);
    }
}

// Initialize the dashboard when the page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('Initializing dashboard...');
    initializeCharts();
    connectWebSocket();
    loadHistoricalData();
    loadSecurityEvents();

    // Add event listeners for historical data controls
    document.getElementById('time-range').addEventListener('change', loadHistoricalData);
    document.getElementById('refresh-history').addEventListener('click', loadHistoricalData);

    // Add event listeners for security events controls
    document.getElementById('security-time-range').addEventListener('change', loadSecurityEvents);
    document.getElementById('refresh-security').addEventListener('click', loadSecurityEvents);
}); 