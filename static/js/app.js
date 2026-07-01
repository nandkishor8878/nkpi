const statusFields = {
    systemStatus: document.querySelector("#system-status"),
    connectionMessage: document.querySelector("#connection-message"),
    robotMode: document.querySelector("#robot-mode"),
    robotUptime: document.querySelector("#robot-uptime"),
    esp32Status: document.querySelector("#esp32-status"),
    cameraStatus: document.querySelector("#camera-status"),
    ledStatus: document.querySelector("#led-status"),
    servo0Status: document.querySelector("#servo-0-status"),
    distanceStatus: document.querySelector("#distance-status"),
    proximityStatus: document.querySelector("#proximity-status"),
    visitorStatus: document.querySelector("#visitor-status"),
    visionStatus: document.querySelector("#vision-status"),
    imuStatus: document.querySelector("#imu-status"),
    imuLinkStatus: document.querySelector("#imu-link-status"),
    pollCount: document.querySelector("#poll-count"),
    pollErrorCount: document.querySelector("#poll-error-count"),
    commandCount: document.querySelector("#command-count"),
    errorCount: document.querySelector("#error-count"),
    lastCommand: document.querySelector("#last-command"),
    lastError: document.querySelector("#last-error"),
    lastUpdated: document.querySelector("#last-updated"),
    eventLog: document.querySelector("#event-log"),
    commandMessage: document.querySelector("#command-message")
};

const dashboardMetrics = {
    pollCount: 0,
    pollErrorCount: 0
};

async function requestJson(url, options = {}) {
    const response = await fetch(url, options);
    const payload = await response.json();

    if (!response.ok) {
        throw new Error(payload.error || "Request failed");
    }

    return payload;
}

async function refreshStatus() {
    try {
        const status = await requestJson("/api/v1/status");
        dashboardMetrics.pollCount += 1;
        renderStatus(status);
    } catch (error) {
        dashboardMetrics.pollErrorCount += 1;
        renderOffline(error.message);
    }
}

function renderStatus(status) {
    statusFields.systemStatus.textContent = status.status;
    statusFields.systemStatus.className = "status-pill online";
    statusFields.connectionMessage.textContent = "Robot API connected";
    statusFields.robotMode.textContent = status.robot.mode;
    statusFields.robotUptime.textContent = formatUptime(status.robot.uptime_seconds);
    statusFields.esp32Status.textContent = status.components.esp32;
    statusFields.cameraStatus.textContent = status.components.camera;
    statusFields.ledStatus.textContent = status.actuators.led;
    statusFields.servo0Status.textContent = formatServo(status.actuators.servos["0"]);
    statusFields.distanceStatus.textContent = formatDistance(status.sensors.distance_cm);
    statusFields.proximityStatus.textContent = formatProximity(status.sensors.proximity_detected);
    statusFields.visitorStatus.textContent = status.visitor || "None";
    statusFields.visionStatus.textContent = formatVision(status.vision);
    statusFields.imuStatus.textContent = formatImu(status.sensors.imu);
    renderDiagnostics(status.diagnostics);
}

function renderOffline(message) {
    statusFields.systemStatus.textContent = "offline";
    statusFields.systemStatus.className = "status-pill offline";
    statusFields.connectionMessage.textContent = message || "Robot API unavailable";
    statusFields.esp32Status.textContent = "--";
    statusFields.pollCount.textContent = dashboardMetrics.pollCount;
    statusFields.pollErrorCount.textContent = dashboardMetrics.pollErrorCount;
}

function formatUptime(seconds) {
    if (typeof seconds !== "number") {
        return "--";
    }

    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds}s`;
}

function formatServo(servo) {
    if (!servo) {
        return "--";
    }

    if (servo.state === "stopped") {
        return "Stopped";
    }

    if (typeof servo.angle !== "number") {
        return "--";
    }

    return `${servo.angle} deg`;
}

function formatDistance(distanceCm) {
    if (typeof distanceCm !== "number") {
        return "--";
    }

    return `${distanceCm.toFixed(1)} cm`;
}

function formatProximity(detected) {
    if (typeof detected !== "boolean") {
        return "--";
    }

    return detected ? "Detected" : "Clear";
}

function formatVision(vision) {
    if (!vision) {
        return "--";
    }

    return `${vision.face_count || 0} face, ${vision.qr_count || 0} QR`;
}

function formatImu(imu) {
    if (!imu) {
        return "--";
    }

    return `A ${imu.accel_x.toFixed(2)}, ${imu.accel_y.toFixed(2)}, ${imu.accel_z.toFixed(2)} | G ${imu.gyro_x.toFixed(2)}, ${imu.gyro_y.toFixed(2)}, ${imu.gyro_z.toFixed(2)}`;
}

function formatImuStatus(imuStatus) {
    if (!imuStatus) {
        return "--";
    }

    const state = imuStatus.connected ? "Connected" : "Missing";
    return `${state} ${imuStatus.address || ""} ${imuStatus.error || ""}`.trim();
}

function renderDiagnostics(diagnostics) {
    statusFields.pollCount.textContent = dashboardMetrics.pollCount;
    statusFields.pollErrorCount.textContent = dashboardMetrics.pollErrorCount;

    if (!diagnostics) {
        return;
    }

    statusFields.commandCount.textContent = diagnostics.command_count;
    statusFields.errorCount.textContent = diagnostics.error_count;
    statusFields.lastCommand.textContent = diagnostics.last_command || "--";
    statusFields.lastError.textContent = diagnostics.last_error || "--";
    statusFields.lastUpdated.textContent = new Date().toLocaleTimeString();
    renderEventLog(diagnostics.recent_events || []);
}

function renderEventLog(events) {
    statusFields.eventLog.replaceChildren();

    events.slice().reverse().forEach((event) => {
        const item = document.createElement("li");
        item.className = `event-${event.level}`;
        const timestamp = new Date(event.timestamp * 1000).toLocaleTimeString();
        item.textContent = `${timestamp} ${event.level.toUpperCase()} ${event.message}`;
        statusFields.eventLog.appendChild(item);
    });
}

async function runCommand(label, callback) {
    statusFields.commandMessage.textContent = `${label}...`;

    try {
        await callback();
        statusFields.commandMessage.textContent = `${label} complete`;
        await refreshStatus();
    } catch (error) {
        statusFields.commandMessage.textContent = `${label} failed: ${error.message}`;
    }
}

async function ledOn() {
    await runCommand("LED on", () => requestJson("/api/v1/led/on", {method: "POST"}));
}

async function ledOff() {
    await runCommand("LED off", () => requestJson("/api/v1/led/off", {method: "POST"}));
}

async function setServoAngle(angle) {
    await runCommand(
        `Servo 0 to ${angle} deg`,
        () => requestJson(
            "/api/v1/servo",
            {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({channel: 0, angle})
            }
        )
    );
}

async function stopServo() {
    await runCommand(
        "Servo stop",
        () => requestJson(
            "/api/v1/servo/stop",
            {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({channel: 0})
            }
        )
    );
}

function servoPositionToAngle(position) {
    const positions = {
        left: 45,
        center: 90,
        right: 135
    };

    return positions[position];
}

async function readDistance() {
    await runCommand("Distance read", () => requestJson("/api/v1/sensors/distance"));
}

async function readProximity() {
    await runCommand("Proximity read", () => requestJson("/api/v1/sensors/proximity"));
}

async function scanVision() {
    await runCommand("Vision scan", () => requestJson("/api/v1/vision/analyze"));
}

async function readImu() {
    await runCommand("IMU read", () => requestJson("/api/v1/sensors/imu"));
}

async function readImuStatus() {
    await runCommand(
        "IMU status",
        async () => {
            const payload = await requestJson("/api/v1/sensors/imu/status");
            statusFields.imuLinkStatus.textContent = formatImuStatus(payload.imu_status);
        }
    );
}

document.querySelector("[data-action='led-on']").addEventListener("click", ledOn);
document.querySelector("[data-action='led-off']").addEventListener("click", ledOff);
document.querySelector("[data-action='servo-stop']").addEventListener("click", stopServo);
document.querySelector("[data-action='read-distance']").addEventListener("click", readDistance);
document.querySelector("[data-action='read-proximity']").addEventListener("click", readProximity);
document.querySelector("[data-action='vision-scan']").addEventListener("click", scanVision);
document.querySelector("[data-action='read-imu']").addEventListener("click", readImu);
document.querySelector("[data-action='read-imu-status']").addEventListener("click", readImuStatus);

document.querySelectorAll("[data-servo-angle]").forEach((button) => {
    button.addEventListener("click", () => {
        setServoAngle(Number(button.dataset.servoAngle));
    });
});

document.querySelectorAll("[data-servo-position]").forEach((button) => {
    button.addEventListener("click", () => {
        setServoAngle(servoPositionToAngle(button.dataset.servoPosition));
    });
});

refreshStatus();
setInterval(refreshStatus, 2000);
