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
    servo_auto_release_after_move: bool = False
    servo_release_delay_seconds: float = 0.35
    pca9685_channels: int = 16
    pca9685_i2c_address: int = 0x40
    proximity_threshold_cm: float = 50.0
    vision_face_scale_factor: float = 1.05
    vision_face_min_neighbors: int = 4
    vision_face_min_size_px: int = 30
    face_tracking_servo_channel: int = 0
    face_tracking_dead_zone_px: int = 50
    face_tracking_step_degrees: int = 4
    face_tracking_invert_servo: bool = False
    face_tracking_smooth: bool = True
    visitor_greeting_message: str = "Hello, welcome. How can I help you today?"
    visitor_greeting_cooldown_seconds: float = 30.0
    visitor_presence_timeout_seconds: float = 5.0
    visitor_greeting_display_seconds: float = 3.0
    speech_provider: str = "espeak"
    speech_enabled: bool = True
    speech_command: str = "espeak-ng"
    speech_voice: str = ""
    speech_speed_wpm: int = 155
    speech_pitch: int = 50
    speech_volume: int = 120
    speech_timeout_seconds: float = 10.0
    speech_max_text_length: int = 240
    visitor_speak_greeting: bool = True
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
            servo_auto_release_after_move=_env_bool(
                "AURA_SERVO_AUTO_RELEASE_AFTER_MOVE", False
            ),
            servo_release_delay_seconds=float(
                os.getenv("AURA_SERVO_RELEASE_DELAY_SECONDS", "0.35")
            ),
            pca9685_channels=int(os.getenv("AURA_PCA9685_CHANNELS", "16")),
            pca9685_i2c_address=int(os.getenv("AURA_PCA9685_I2C_ADDRESS", "0x40"), 0),
            proximity_threshold_cm=float(os.getenv("AURA_PROXIMITY_THRESHOLD_CM", "50")),
            vision_face_scale_factor=float(
                os.getenv("AURA_VISION_FACE_SCALE_FACTOR", "1.05")
            ),
            vision_face_min_neighbors=int(
                os.getenv("AURA_VISION_FACE_MIN_NEIGHBORS", "4")
            ),
            vision_face_min_size_px=int(os.getenv("AURA_VISION_FACE_MIN_SIZE_PX", "30")),
            face_tracking_servo_channel=int(
                os.getenv("AURA_FACE_TRACKING_SERVO_CHANNEL", "0")
            ),
            face_tracking_dead_zone_px=int(
                os.getenv("AURA_FACE_TRACKING_DEAD_ZONE_PX", "50")
            ),
            face_tracking_step_degrees=int(
                os.getenv("AURA_FACE_TRACKING_STEP_DEGREES", "4")
            ),
            face_tracking_invert_servo=_env_bool(
                "AURA_FACE_TRACKING_INVERT_SERVO", False
            ),
            face_tracking_smooth=_env_bool("AURA_FACE_TRACKING_SMOOTH", True),
            visitor_greeting_message=os.getenv(
                "AURA_VISITOR_GREETING_MESSAGE",
                "Hello, welcome. How can I help you today?",
            ),
            visitor_greeting_cooldown_seconds=float(
                os.getenv("AURA_VISITOR_GREETING_COOLDOWN_SECONDS", "30")
            ),
            visitor_presence_timeout_seconds=float(
                os.getenv("AURA_VISITOR_PRESENCE_TIMEOUT_SECONDS", "5")
            ),
            visitor_greeting_display_seconds=float(
                os.getenv("AURA_VISITOR_GREETING_DISPLAY_SECONDS", "3")
            ),
            speech_provider=os.getenv("AURA_SPEECH_PROVIDER", "espeak"),
            speech_enabled=_env_bool("AURA_SPEECH_ENABLED", True),
            speech_command=os.getenv("AURA_SPEECH_COMMAND", "espeak-ng"),
            speech_voice=os.getenv("AURA_SPEECH_VOICE", ""),
            speech_speed_wpm=int(os.getenv("AURA_SPEECH_SPEED_WPM", "155")),
            speech_pitch=int(os.getenv("AURA_SPEECH_PITCH", "50")),
            speech_volume=int(os.getenv("AURA_SPEECH_VOLUME", "120")),
            speech_timeout_seconds=float(os.getenv("AURA_SPEECH_TIMEOUT_SECONDS", "10")),
            speech_max_text_length=int(os.getenv("AURA_SPEECH_MAX_TEXT_LENGTH", "240")),
            visitor_speak_greeting=_env_bool("AURA_VISITOR_SPEAK_GREETING", True),
            testing=_env_bool("AURA_TESTING", False),
        )
