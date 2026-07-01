from dataclasses import dataclass
import os


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    flask_host: str = "0.0.0.0"
    flask_port: int = 5000
    camera_provider: str = "pi"
    camera_width: int = 640
    camera_height: int = 480
    serial_transport: str = "serial"
    serial_port: str = "/dev/ttyUSB0"
    serial_baudrate: int = 115200
    serial_timeout_seconds: float = 1.0
    hardware_startup_delay_seconds: float = 2.0
    servo_driver: str = "pca9685"
    servo_default_channel: int = 0
    servo_min_angle: int = 0
    servo_max_angle: int = 180
    servo_left_angle: int = 45
    servo_center_angle: int = 90
    servo_right_angle: int = 135
    servo_smooth_step_degrees: int = 2
    servo_smooth_step_delay_seconds: float = 0.02
    pca9685_channels: int = 16
    pca9685_i2c_address: int = 0x40
    proximity_threshold_cm: float = 50.0
    testing: bool = False

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            flask_host=os.getenv("AURA_FLASK_HOST", "0.0.0.0"),
            flask_port=int(os.getenv("AURA_FLASK_PORT", "5000")),
            camera_provider=os.getenv("AURA_CAMERA_PROVIDER", "pi"),
            camera_width=int(os.getenv("AURA_CAMERA_WIDTH", "640")),
            camera_height=int(os.getenv("AURA_CAMERA_HEIGHT", "480")),
            serial_transport=os.getenv("AURA_SERIAL_TRANSPORT", "serial"),
            serial_port=os.getenv("AURA_SERIAL_PORT", "/dev/ttyUSB0"),
            serial_baudrate=int(os.getenv("AURA_SERIAL_BAUDRATE", "115200")),
            serial_timeout_seconds=float(os.getenv("AURA_SERIAL_TIMEOUT_SECONDS", "1")),
            hardware_startup_delay_seconds=float(
                os.getenv("AURA_HARDWARE_STARTUP_DELAY_SECONDS", "2")
            ),
            servo_driver=os.getenv("AURA_SERVO_DRIVER", "pca9685"),
            servo_default_channel=int(os.getenv("AURA_SERVO_DEFAULT_CHANNEL", "0")),
            servo_min_angle=int(os.getenv("AURA_SERVO_MIN_ANGLE", "0")),
            servo_max_angle=int(os.getenv("AURA_SERVO_MAX_ANGLE", "180")),
            servo_left_angle=int(os.getenv("AURA_SERVO_LEFT_ANGLE", "45")),
            servo_center_angle=int(os.getenv("AURA_SERVO_CENTER_ANGLE", "90")),
            servo_right_angle=int(os.getenv("AURA_SERVO_RIGHT_ANGLE", "135")),
            servo_smooth_step_degrees=int(os.getenv("AURA_SERVO_SMOOTH_STEP_DEGREES", "2")),
            servo_smooth_step_delay_seconds=float(
                os.getenv("AURA_SERVO_SMOOTH_STEP_DELAY_SECONDS", "0.02")
            ),
            pca9685_channels=int(os.getenv("AURA_PCA9685_CHANNELS", "16")),
            pca9685_i2c_address=int(os.getenv("AURA_PCA9685_I2C_ADDRESS", "0x40"), 0),
            proximity_threshold_cm=float(os.getenv("AURA_PROXIMITY_THRESHOLD_CM", "50")),
            testing=_env_bool("AURA_TESTING", False),
        )
