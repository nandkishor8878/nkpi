# ESP32 Firmware

Firmware lives in `firmware/esp32/aura_controller`.

## Arduino Libraries

Install these libraries from Arduino IDE Library Manager:

- `Adafruit PWM Servo Driver Library`
- `Adafruit BusIO`

## Supported Serial Commands

Commands are newline-delimited and use `115200` baud.

| Command | Response | Purpose |
| --- | --- | --- |
| `PING` | `PONG` | Communication health check |
| `LED_ON` | `OK` | Turn ESP32 status LED on |
| `LED_OFF` | `OK` | Turn ESP32 status LED off |
| `SERVO:0:90` | `OK` | Move PCA9685 servo channel 0 to 90 degrees |

Invalid commands return an `ERROR:...` response.

## PCA9685 Wiring

Typical ESP32 DevKit V1 I2C wiring:

| ESP32 | PCA9685 |
| --- | --- |
| `3V3` | `VCC` |
| `GND` | `GND` |
| `GPIO 21` | `SDA` |
| `GPIO 22` | `SCL` |

Servo power should come from a separate suitable supply connected to PCA9685 `V+`.
Do not power servos directly from the ESP32.
Make sure ESP32 ground and servo supply ground are connected.

## Servo Command Contract

The Raspberry Pi API endpoint:

`POST /api/v1/servos/{servo_id}/angle`

with:

```json
{"angle": 90}
```

sends this ESP32 command:

```text
SERVO:<servo_id>:<angle>
```

The firmware accepts PCA9685 channels `0` through `15` and servo angles `0` through `180`.

## Calibration

Default pulse range:

- min: `500 us`
- max: `2500 us`
- frequency: `50 Hz`

Tune these values in `config.h` if your servo does not reach the expected physical range or makes noise at the endpoints.

