# Deployment

## Raspberry Pi Dependency Update

After pulling new code on the Raspberry Pi, activate the project virtual
environment and install dependencies:

```bash
cd ~/smart-reception-assistant
source .venv/bin/activate
pip install -r requirements.txt
```

The direct Raspberry Pi PCA9685 servo driver requires:

```text
adafruit-circuitpython-servokit
```

Speech output requires a local TTS command on the Raspberry Pi:

```bash
sudo apt update
sudo apt install -y espeak-ng alsa-utils
```

The import used by the application is:

```python
from adafruit_servokit import ServoKit
```

If the dependency is missing, the app will start with the servo controller marked
unavailable so camera streaming and other APIs keep working.

## Environment Profiles

Development/mock profile:

```bash
config/env/development.env
```

Production/Raspberry Pi profile:

```bash
config/env/production.env
```

The production profile uses:

```text
AURA_CAMERA_PROVIDER=pi
AURA_SERIAL_TRANSPORT=serial
AURA_SERVO_DRIVER=pca9685
```

The development profile uses mock hardware so the dashboard can run without
physical devices.

## Servo Calibration

Current conservative production defaults:

```text
AURA_SERVO_MIN_ANGLE=30
AURA_SERVO_MAX_ANGLE=150
AURA_SERVO_LEFT_ANGLE=60
AURA_SERVO_CENTER_ANGLE=90
AURA_SERVO_RIGHT_ANGLE=120
AURA_SERVO_AUTO_RELEASE_AFTER_MOVE=true
AURA_SERVO_RELEASE_DELAY_SECONDS=0.35
```

Check the active calibration:

```bash
curl http://localhost:5000/api/v1/servo/calibration
```

Test safe positions:

```bash
curl -X POST http://localhost:5000/api/v1/servo \
  -H "Content-Type: application/json" \
  -d '{"channel":0,"angle":90,"smooth":false}'
```

If the servo hits its physical stop, reduce `AURA_SERVO_MIN_ANGLE` and
`AURA_SERVO_MAX_ANGLE` in `config/env/production.env`, then restart the service.

If the servo keeps rotating after an angle command, first confirm it is a
positional MG90S and not a 360-degree continuous-rotation servo. The production
profile releases PWM after each completed move:

```text
AURA_SERVO_AUTO_RELEASE_AFTER_MOVE=true
AURA_SERVO_RELEASE_DELAY_SECONDS=0.35
```

Increase `AURA_SERVO_RELEASE_DELAY_SECONDS` if the positional servo does not get
enough time to reach the target before PWM is released.

## Systemd Service

Install and start the service:

```bash
cd ~/smart-reception-assistant
bash deploy/systemd/install_service.sh
```

Useful commands:

```bash
sudo systemctl status aura.service
sudo systemctl restart aura.service
sudo systemctl stop aura.service
journalctl -u aura.service -f
```

After editing `config/env/production.env`:

```bash
sudo systemctl restart aura.service
```

## Face Tracking Tuning

Face tracking uses the camera frame and the configured pan servo channel:

```text
AURA_FACE_TRACKING_SERVO_CHANNEL=0
AURA_FACE_TRACKING_DEAD_ZONE_PX=50
AURA_FACE_TRACKING_STEP_DEGREES=4
AURA_FACE_TRACKING_INVERT_SERVO=false
AURA_FACE_TRACKING_SMOOTH=true
```

Face detection sensitivity is controlled by:

```text
AURA_VISION_FACE_SCALE_FACTOR=1.05
AURA_VISION_FACE_MIN_NEIGHBORS=4
AURA_VISION_FACE_MIN_SIZE_PX=30
```

If faces are still missed, lower `AURA_VISION_FACE_MIN_NEIGHBORS` to `3`. If
false detections appear, raise it to `5` or `6`.

If the camera turns away from a face instead of toward it, change:

```text
AURA_FACE_TRACKING_INVERT_SERVO=true
```

Then restart:

```bash
sudo systemctl restart aura.service
```

## Visitor Greeting

Visitor checks use face tracking and the configured greeting text:

```text
AURA_VISITOR_GREETING_MESSAGE=Hello, welcome. How can I help you today?
AURA_VISITOR_GREETING_COOLDOWN_SECONDS=30
AURA_VISITOR_PRESENCE_TIMEOUT_SECONDS=5
AURA_VISITOR_GREETING_DISPLAY_SECONDS=3
AURA_VISITOR_SPEAK_GREETING=true

AURA_SPEECH_PROVIDER=espeak
AURA_SPEECH_ENABLED=true
AURA_SPEECH_COMMAND=espeak-ng
AURA_SPEECH_VOICE=
AURA_SPEECH_SPEED_WPM=155
AURA_SPEECH_PITCH=50
AURA_SPEECH_VOLUME=120
AURA_SPEECH_TIMEOUT_SECONDS=10
AURA_SPEECH_MAX_TEXT_LENGTH=240
```

Manual test:

```bash
curl -X POST http://localhost:5000/api/v1/visitor/check \
  -H "Content-Type: application/json" \
  -d '{"track":true}'
```

Read current visitor state:

```bash
curl http://localhost:5000/api/v1/visitor/status
```

Manual speech test:

```bash
curl -X POST http://localhost:5000/api/v1/speech/say \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello, welcome. How can I help you today?"}'
```

If the API returns success but no sound is heard, verify the Pi audio output:

```bash
aplay -l
speaker-test -t wav -c 2
```

## Visitor Listening

Audio input uses ALSA `arecord`:

```text
AURA_AUDIO_RECORDER_PROVIDER=arecord
AURA_AUDIO_ENABLED=true
AURA_AUDIO_COMMAND=arecord
AURA_AUDIO_DEVICE=default
AURA_AUDIO_RECORDINGS_DIR=/tmp/aura/audio
AURA_AUDIO_SAMPLE_RATE=16000
AURA_AUDIO_CHANNELS=1
AURA_AUDIO_FORMAT=S16_LE
AURA_AUDIO_DEFAULT_DURATION_SECONDS=4
AURA_AUDIO_MAX_DURATION_SECONDS=8
```

The first speech recognition provider is mock-backed:

```text
AURA_SPEECH_RECOGNITION_PROVIDER=mock
AURA_SPEECH_RECOGNITION_ENABLED=true
```

Check microphone devices:

```bash
arecord -l
```

Manual recording test:

```bash
arecord -D default -f S16_LE -r 16000 -c 1 -d 4 /tmp/aura-test.wav
aplay /tmp/aura-test.wav
```

API recording test:

```bash
curl -X POST http://localhost:5000/api/v1/audio/record \
  -H "Content-Type: application/json" \
  -d '{"duration_seconds":4}'
```

End-to-end listen/transcript test:

```bash
curl -X POST http://localhost:5000/api/v1/speech/listen \
  -H "Content-Type: application/json" \
  -d '{"duration_seconds":4}'
```

With the mock recognizer, this returns the configured mock transcript. Replace
the recognizer provider later when the microphone path is verified.
