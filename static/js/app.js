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
    visitorStatus: document.querySelector("#visitor-status"),
    imuStatus: document.querySelector("#imu-status"),
    commandMessage: document.querySelector("#command-message")
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
        renderStatus(status);
    } catch (error) {
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
    statusFields.visitorStatus.textContent = status.visitor || "None";
    statusFields.imuStatus.textContent = formatImu(status.sensors.imu);
}

function renderOffline(message) {
    statusFields.systemStatus.textContent = "offline";
    statusFields.systemStatus.className = "status-pill offline";
    statusFields.connectionMessage.textContent = message || "Robot API unavailable";
    statusFields.esp32Status.textContent = "--";
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
    if (!servo || typeof servo.angle !== "number") {
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

function formatImu(imu) {
    if (!imu) {
        return "--";
    }

    return `A ${imu.accel_x.toFixed(2)}, ${imu.accel_y.toFixed(2)}, ${imu.accel_z.toFixed(2)} | G ${imu.gyro_x.toFixed(2)}, ${imu.gyro_y.toFixed(2)}, ${imu.gyro_z.toFixed(2)}`;
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
            "/api/v1/servos/0/angle",
            {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({angle})
            }
        )
    );
}

async function readDistance() {
    await runCommand("Distance read", () => requestJson("/api/v1/sensors/distance"));
}

async function readImu() {
    await runCommand("IMU read", () => requestJson("/api/v1/sensors/imu"));
}

document.querySelector("[data-action='led-on']").addEventListener("click", ledOn);
document.querySelector("[data-action='led-off']").addEventListener("click", ledOff);
document.querySelector("[data-action='read-distance']").addEventListener("click", readDistance);
document.querySelector("[data-action='read-imu']").addEventListener("click", readImu);

document.querySelectorAll("[data-servo-angle]").forEach((button) => {
    button.addEventListener("click", () => {
        setServoAngle(Number(button.dataset.servoAngle));
    });
});

refreshStatus();
setInterval(refreshStatus, 2000);
