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
| `READ:DISTANCE` | `DISTANCE_CM:42.7` | Read HC-SR04 distance in centimeters |
| `READ:IMU` | `IMU:AX:0.01:AY:0.02:AZ:1.00:GX:0.10:GY:0.20:GZ:0.30` | Read MPU6050 accelerometer and gyro |

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

## HC-SR04 Wiring

Default firmware pins:

| ESP32 | HC-SR04 |
| --- | --- |
| `5V` | `VCC` |
| `GND` | `GND` |
| `GPIO 5` | `TRIG` |
| `GPIO 18` | `ECHO` through voltage divider or level shifter |

Important: many HC-SR04 modules output 5V on `ECHO`. ESP32 GPIO is 3.3V only.
Use a voltage divider or level shifter before connecting `ECHO` to the ESP32.

## MPU6050 Wiring

The MPU6050 uses the same ESP32 I2C bus as the PCA9685.

| ESP32 | MPU6050 |
| --- | --- |
| `3V3` | `VCC` |
| `GND` | `GND` |
| `GPIO 21` | `SDA` |
| `GPIO 22` | `SCL` |

Default I2C address is `0x68`.

## Servo Command Contract

The Raspberry Pi API endpoint:

`POST /api/v1/servo`

with:

```json
{"channel": 0, "angle": 90}
```

directly controls the PCA9685 when `AURA_SERVO_DRIVER=pca9685`.

The compatibility endpoint:

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

For the current hardware setup, PCA9685 is connected to Raspberry Pi I2C and
detected at address `0x40`, so the direct Pi driver is preferred.

## Calibration

Default pulse range:

- min: `500 us`
- max: `2500 us`
- frequency: `50 Hz`

Tune these values in `config.h` if your servo does not reach the expected physical range or makes noise at the endpoints.

Distance timeout and pins are also configured in `config.h`.
