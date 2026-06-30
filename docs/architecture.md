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
- `POST /api/v1/led/on`
- `POST /api/v1/led/off`
- `POST /api/v1/servos/{servo_id}/angle` with JSON body `{"angle": 90}`

## Next Expansion Points

- Add servo control as an actuator adapter and application service method.
- Add ultrasonic and IMU access as sensor adapters.
- Promote the ESP32 protocol from plain command strings to framed messages with request ids.
- Add OpenAPI documentation once the first stable API set is complete.

## Servo Control

Servo commands flow through:

`servo_routes -> RobotControlService -> ServoController -> CommandTransportPort`

The controller validates servo ids and angle limits before sending hardware commands.
The current ESP32 command is `SERVO:<servo_id>:<angle>`, kept behind
`Esp32Protocol` so the protocol can evolve without changing HTTP routes.

The ESP32 firmware side mirrors this with:

`aura_controller.ino -> CommandDispatcher -> ServoController -> PCA9685`
