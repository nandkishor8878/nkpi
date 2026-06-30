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
    servo_min_angle: int = 0
    servo_max_angle: int = 180
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
            servo_min_angle=int(os.getenv("AURA_SERVO_MIN_ANGLE", "0")),
            servo_max_angle=int(os.getenv("AURA_SERVO_MAX_ANGLE", "180")),
            testing=_env_bool("AURA_TESTING", False),
        )
