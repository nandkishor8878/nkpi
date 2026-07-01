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
