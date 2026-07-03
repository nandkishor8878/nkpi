import atexit

from flask import Flask

from aura.api.dependencies import AppContainer
from aura.api.routes.audio_routes import audio_bp
from aura.api.routes.camera_routes import camera_bp
from aura.api.routes.face_tracking_routes import face_tracking_bp
from aura.api.routes.health_routes import health_bp
from aura.api.routes.led_routes import led_bp
from aura.api.routes.servo_routes import servo_bp
from aura.api.routes.sensor_routes import sensor_bp
from aura.api.routes.speech_routes import speech_bp
from aura.api.routes.status_routes import status_bp
from aura.api.routes.visitor_routes import visitor_bp
from aura.api.routes.vision_routes import vision_bp
from aura.api.routes.web_routes import web_bp
from aura.application.services.camera_stream_service import CameraStreamService
from aura.application.services.audio_service import AudioService
from aura.application.services.face_tracking_service import FaceTrackingService
from aura.application.services.health_service import HealthService
from aura.application.services.robot_control_service import RobotControlService
from aura.application.services.robot_state_store import RobotStateStore
from aura.application.services.robot_status_service import RobotStatusService
from aura.application.services.servo_service import ServoService
from aura.application.services.sensor_service import SensorService
from aura.application.services.speech_service import SpeechService
from aura.application.services.speech_recognition_service import SpeechRecognitionService
from aura.application.services.visitor_service import VisitorService
from aura.application.services.vision_service import VisionService
from aura.config.settings import Settings
from aura.infrastructure.actuators.mock_servo_controller import MockServoController
from aura.infrastructure.actuators.pca9685_servo_controller import Pca9685ServoController
from aura.infrastructure.actuators.servo_controller import ServoController
from aura.infrastructure.audio.arecord_audio_recorder import ArecordAudioRecorder
from aura.infrastructure.audio.espeak_speech_synthesizer import EspeakSpeechSynthesizer
from aura.infrastructure.audio.mock_audio_recorder import MockAudioRecorder
from aura.infrastructure.audio.mock_speech_synthesizer import MockSpeechSynthesizer
from aura.infrastructure.audio.mock_speech_recognizer import MockSpeechRecognizer
from aura.infrastructure.camera.mock_camera import MockCamera
from aura.infrastructure.camera.pi_camera import PiCamera
from aura.infrastructure.communication.mock_transport import MockTransport
from aura.infrastructure.communication.serial_transport import SerialTransport
from aura.infrastructure.sensors.imu_sensor_client import ImuSensorClient
from aura.infrastructure.sensors.ultrasonic_sensor_client import UltrasonicSensorClient


def create_app(settings: Settings | None = None) -> Flask:
    settings = settings or Settings.from_env()

    app = Flask(
        __name__,
        template_folder="../../templates",
        static_folder="../../static",
    )
    app.config["TESTING"] = settings.testing

    container = _build_container(settings)
    app.extensions["aura"] = container
    if not settings.testing:
        atexit.register(container.close)

    app.register_blueprint(web_bp)
    app.register_blueprint(audio_bp)
    app.register_blueprint(camera_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(led_bp)
    app.register_blueprint(servo_bp)
    app.register_blueprint(sensor_bp)
    app.register_blueprint(speech_bp)
    app.register_blueprint(vision_bp)
    app.register_blueprint(face_tracking_bp)
    app.register_blueprint(visitor_bp)

    return app


def _build_container(settings: Settings) -> AppContainer:
    camera = _build_camera(settings)
    transport = _build_transport(settings)
    servo_controller = _build_servo_controller(settings, transport)
    ultrasonic_sensor = UltrasonicSensorClient(transport)
    imu_sensor = ImuSensorClient(transport)
    state_store = RobotStateStore()
    health_service = HealthService(transport)
    camera_stream_service = CameraStreamService(camera)
    robot_control_service = RobotControlService(
        transport,
        servo_controller,
        state_store,
    )
    servo_service = ServoService(servo_controller, state_store, settings)
    vision_service = VisionService(camera_stream_service, state_store, settings)
    face_tracking_service = FaceTrackingService(
        vision_service,
        servo_service,
        state_store,
        settings,
    )
    audio_service = AudioService(
        _build_audio_recorder(settings),
        state_store,
        settings,
    )
    speech_service = SpeechService(
        _build_speech_synthesizer(settings),
        state_store,
        settings,
    )
    speech_recognition_service = SpeechRecognitionService(
        audio_service,
        _build_speech_recognizer(settings),
        state_store,
        settings,
    )
    visitor_service = VisitorService(
        face_tracking_service,
        state_store,
        settings,
        speech_service,
    )
    return AppContainer(
        settings=settings,
        camera=camera,
        transport=transport,
        servo_controller=servo_controller,
        state_store=state_store,
        camera_stream_service=camera_stream_service,
        health_service=health_service,
        robot_control_service=robot_control_service,
        servo_service=servo_service,
        robot_status_service=RobotStatusService(state_store, health_service),
        sensor_service=SensorService(ultrasonic_sensor, imu_sensor, state_store, settings),
        audio_service=audio_service,
        speech_service=speech_service,
        speech_recognition_service=speech_recognition_service,
        vision_service=vision_service,
        face_tracking_service=face_tracking_service,
        visitor_service=visitor_service,
    )


def _build_camera(settings: Settings):
    if settings.camera_provider == "mock":
        return MockCamera()
    return PiCamera(settings)


def _build_transport(settings: Settings):
    if settings.serial_transport == "mock":
        return MockTransport()
    return SerialTransport(settings)


def _build_servo_controller(settings: Settings, transport):
    if settings.testing or settings.servo_driver == "mock":
        return MockServoController(settings)
    if settings.servo_driver == "serial":
        return ServoController(transport, settings)
    if settings.servo_driver == "pca9685":
        return Pca9685ServoController(settings)
    raise ValueError(f"Unsupported servo driver: {settings.servo_driver}")


def _build_speech_synthesizer(settings: Settings):
    if settings.testing or settings.speech_provider == "mock":
        return MockSpeechSynthesizer(settings)
    if settings.speech_provider == "espeak":
        return EspeakSpeechSynthesizer(settings)
    raise ValueError(f"Unsupported speech provider: {settings.speech_provider}")


def _build_audio_recorder(settings: Settings):
    if settings.testing or settings.audio_recorder_provider == "mock":
        return MockAudioRecorder(settings)
    if settings.audio_recorder_provider == "arecord":
        return ArecordAudioRecorder(settings)
    raise ValueError(f"Unsupported audio recorder provider: {settings.audio_recorder_provider}")


def _build_speech_recognizer(settings: Settings):
    if settings.speech_recognition_provider == "mock":
        return MockSpeechRecognizer(settings)
    raise ValueError(
        f"Unsupported speech recognition provider: {settings.speech_recognition_provider}"
    )
