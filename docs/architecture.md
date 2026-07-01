# Project Aura Architecture

Project Aura is organized as a robotics platform, not a single Flask app.

## Layers

- `aura.api`: HTTP routes and Flask app factory.
- `aura.application`: use-case services that coordinate robot behavior.
- `aura.domain`: stable interfaces and robot concepts.
- `aura.infrastructure`: hardware, serial, camera, and external adapters.

## Rules

- Flask routes stay thin and call application services.
- Application services depend on ports, not concrete hardware libraries.
- Hardware drivers live in infrastructure adapters.
- Configuration is loaded through `Settings`, not hardcoded inside routes.
- Tests use mock adapters so they can run without Raspberry Pi hardware.

## Current API

- `GET /`
- `GET /api/v1/camera/stream`
- `GET /video` for backward-compatible camera streaming.
- `GET /api/v1/health`
- `GET /api/v1/status`
- `POST /api/v1/led/on`
- `POST /api/v1/led/off`
- `POST /api/v1/servo` with JSON body `{"channel": 0, "angle": 90}`
- `POST /api/v1/servos/{servo_id}/angle` with JSON body `{"angle": 90}`
- `GET /api/v1/sensors/distance`
- `GET /api/v1/sensors/imu`

## Next Expansion Points

- Add servo control as an actuator adapter and application service method.
- Add ultrasonic and IMU access as sensor adapters.
- Promote the ESP32 protocol from plain command strings to framed messages with request ids.
- Add OpenAPI documentation once the first stable API set is complete.

## Servo Control

Servo commands flow through:

`servo_routes -> ServoService -> ServoPort`

The default hardware driver is Raspberry Pi direct PCA9685 control via
`adafruit_servokit`. Use `AURA_SERVO_DRIVER=pca9685` when the PCA9685 is on the
Pi I2C bus at `0x40`, which matches the current hardware setup.

The older ESP32 serial driver remains available with `AURA_SERVO_DRIVER=serial`.
It sends `SERVO:<servo_id>:<angle>` through `CommandTransportPort` for setups
where the PCA9685 is wired to ESP32 instead of the Pi.

`ServoService` validates angle limits, supports smooth movement, updates robot
state after successful movement, and keeps Flask routes thin.

The ESP32 firmware side mirrors this with:

`aura_controller.ino -> CommandDispatcher -> ServoController -> PCA9685`

## Operator Console State

The browser dashboard polls `GET /api/v1/status` and renders the returned robot
state. Browser controls do not contain robot logic; they call APIs and refresh
status after commands complete.

Current status flow:

`status_routes -> RobotStatusService -> RobotStateStore + HealthService`

Command services update `RobotStateStore` after successful hardware responses.
Future telemetry from sensors can update the same store without changing the
dashboard contract.

## Distance Sensor

Distance reads flow through:

`sensor_routes -> SensorService -> UltrasonicSensorClient -> CommandTransportPort`

The Raspberry Pi sends `READ:DISTANCE` to the ESP32. The ESP32 responds with
`DISTANCE_CM:<value>` or `ERROR:DISTANCE_TIMEOUT`.

Successful reads update `RobotStateStore`, so the dashboard can render distance
through `GET /api/v1/status`.

IMU reads use the same route/service/client structure. The Raspberry Pi sends
`READ:IMU`; the ESP32 responds with accel and gyro fields in one line:

`IMU:AX:<x>:AY:<y>:AZ:<z>:GX:<x>:GY:<y>:GZ:<z>`
