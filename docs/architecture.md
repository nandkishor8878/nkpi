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
- `GET /api/v1/audio/status`
- `POST /api/v1/audio/record`
- `GET /api/v1/camera/stream`
- `GET /video` for backward-compatible camera streaming.
- `GET /api/v1/health`
- `GET /api/v1/status`
- `POST /api/v1/led/on`
- `POST /api/v1/led/off`
- `POST /api/v1/servo` with JSON body `{"channel": 0, "angle": 90}`
- `POST /api/v1/servo/stop` with JSON body `{"channel": 0}`
- `GET /api/v1/servo/calibration`
- `POST /api/v1/servos/{servo_id}/angle` with JSON body `{"angle": 90}`
- `GET /api/v1/sensors/distance`
- `GET /api/v1/sensors/proximity`
- `GET /api/v1/sensors/imu`
- `GET /api/v1/sensors/imu/status`
- `GET /api/v1/speech/status`
- `POST /api/v1/speech/say`
- `POST /api/v1/speech/listen`
- `GET /api/v1/vision/analyze`
- `GET /api/v1/face-tracking/status`
- `POST /api/v1/face-tracking/track`
- `GET /api/v1/visitor/status`
- `POST /api/v1/visitor/check`
- `POST /api/v1/visitor/reset`

## Next Expansion Points

- Add object/person detection models behind `VisionService`.
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

`POST /api/v1/servo/stop` releases the PCA9685 PWM signal for the requested
channel when using the direct Raspberry Pi driver. This is different from
Center, which moves the servo to the configured center angle.

For positional servos that jitter or continuous-rotation servos that keep
spinning, production can enable `AURA_SERVO_AUTO_RELEASE_AFTER_MOVE=true`.
That holds the final angle command briefly, then releases the PCA9685 PWM signal
without forgetting the last commanded angle in robot state.

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

The status payload also includes diagnostics:

- command count
- error count
- last command
- last error
- recent event log

The dashboard adds client-side poll metrics and displays backend diagnostics in
the Diagnostics panel.

## Distance Sensor

Distance reads flow through:

`sensor_routes -> SensorService -> UltrasonicSensorClient -> CommandTransportPort`

The Raspberry Pi sends `READ:DISTANCE` to the ESP32. The ESP32 responds with
`DISTANCE_CM:<value>` or `ERROR:DISTANCE_TIMEOUT`.

Successful reads update `RobotStateStore`, so the dashboard can render distance
through `GET /api/v1/status`.

Proximity is derived from the HC-SR04 distance reading using
`AURA_PROXIMITY_THRESHOLD_CM`. `GET /api/v1/sensors/proximity` returns whether
something is within the configured threshold and updates robot state.

IMU reads use the same route/service/client structure. The Raspberry Pi sends
`READ:IMU`; the ESP32 responds with accel and gyro fields in one line:

`IMU:AX:<x>:AY:<y>:AZ:<z>:GX:<x>:GY:<y>:GZ:<z>`

`GET /api/v1/sensors/imu/status` sends `READ:IMU_STATUS` so wiring/address
issues can be diagnosed without guessing.

## Vision

Vision scans flow through:

`vision_routes -> VisionService -> CameraStreamService -> CameraPort`

The first vision phase supports:

- face detection count and boxes using OpenCV Haar cascade
- QR code decoding using OpenCV `QRCodeDetector`

Face detection applies grayscale contrast normalization before detection and
uses configurable Haar parameters so the Raspberry Pi camera can be tuned
without code changes.

Successful scans update `RobotStateStore`, so `GET /api/v1/status` includes
the latest vision snapshot and visitor state. Future object detection models can
be added behind `VisionService` without changing dashboard/API consumers.

## Face Tracking

Face tracking flows through:

`face_tracking_routes -> FaceTrackingService -> VisionService + ServoService`

`FaceTrackingService` chooses the largest detected face, compares its horizontal
center to the frame center, and moves the configured pan servo by a small
configurable step only when the face is outside the dead zone. This keeps the
Flask route thin and keeps camera analysis separate from actuator control.

Important tuning settings:

- `AURA_FACE_TRACKING_SERVO_CHANNEL`
- `AURA_FACE_TRACKING_DEAD_ZONE_PX`
- `AURA_FACE_TRACKING_STEP_DEGREES`
- `AURA_FACE_TRACKING_INVERT_SERVO`
- `AURA_FACE_TRACKING_SMOOTH`

The dashboard supports a single Track command and browser-driven Auto tracking.
Auto tracking calls the same one-shot API on a timer, so stopping it from the UI
does not require killing a backend worker.

## Visitor Flow

Visitor checks flow through:

`visitor_routes -> VisitorService -> FaceTrackingService -> VisionService + ServoService`

`VisitorService` is the first receptionist behavior layer. It checks whether a
face is present, lets face tracking center the camera, updates structured
visitor state, and produces a text greeting with a cooldown so Aura does not
repeat itself every dashboard poll.

Visitor states:

- `no_visitor`
- `visitor_detected`
- `greeting`
- `waiting_for_response`

Important tuning settings:

- `AURA_VISITOR_GREETING_MESSAGE`
- `AURA_VISITOR_GREETING_COOLDOWN_SECONDS`
- `AURA_VISITOR_PRESENCE_TIMEOUT_SECONDS`
- `AURA_VISITOR_GREETING_DISPLAY_SECONDS`

The current greeting is text-only and displayed on the dashboard. This is the
extension point for speech-to-text, appointment lookup, known-face profiles,
and Android notifications.

## Audio Input

Audio recording flows through:

`audio_routes -> AudioService -> AudioRecorderPort`

Production uses the local `arecord` command from ALSA. Development and tests use
`MockAudioRecorder`. The audio layer only records and reports metadata; it does
not perform speech recognition directly.

Important tuning settings:

- `AURA_AUDIO_RECORDER_PROVIDER`
- `AURA_AUDIO_ENABLED`
- `AURA_AUDIO_COMMAND`
- `AURA_AUDIO_DEVICE`
- `AURA_AUDIO_RECORDINGS_DIR`
- `AURA_AUDIO_SAMPLE_RATE`
- `AURA_AUDIO_CHANNELS`
- `AURA_AUDIO_DEFAULT_DURATION_SECONDS`
- `AURA_AUDIO_MAX_DURATION_SECONDS`

## Speech Output

Speech output flows through:

`speech_routes -> SpeechService -> SpeechPort`

The production speech adapter uses the local `espeak-ng` command, which keeps
the Raspberry Pi working offline. Tests and development use
`MockSpeechSynthesizer`.

`VisitorService` composes `SpeechService`, so a generated greeting can be spoken
at the same time it is written into visitor state. Speech output is also exposed
directly through `POST /api/v1/speech/say` for dashboard/manual tests.

Important tuning settings:

- `AURA_SPEECH_PROVIDER`
- `AURA_SPEECH_ENABLED`
- `AURA_SPEECH_COMMAND`
- `AURA_SPEECH_VOICE`
- `AURA_SPEECH_SPEED_WPM`
- `AURA_SPEECH_PITCH`
- `AURA_SPEECH_VOLUME`
- `AURA_VISITOR_SPEAK_GREETING`

## Speech Recognition

Visitor listening flows through:

`speech_routes -> SpeechRecognitionService -> AudioService + SpeechRecognitionPort`

The first recognizer is intentionally mock-backed. It validates the complete
record/listen/transcript flow before a heavier STT engine is added. A future
Vosk, Whisper, or cloud recognizer can replace `MockSpeechRecognizer` without
changing dashboard, visitor, or audio recording contracts.

`POST /api/v1/speech/listen` records a short audio clip, transcribes it, stores
the recognition result, and writes the latest transcript into visitor state.
