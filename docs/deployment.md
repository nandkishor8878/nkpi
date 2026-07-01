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
