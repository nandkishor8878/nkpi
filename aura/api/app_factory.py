import atexit

from flask import Flask

from aura.api.dependencies import AppContainer
from aura.api.routes.camera_routes import camera_bp
from aura.api.routes.health_routes import health_bp
from aura.api.routes.led_routes import led_bp
from aura.api.routes.servo_routes import servo_bp
from aura.api.routes.sensor_routes import sensor_bp
from aura.api.routes.status_routes import status_bp
from aura.api.routes.web_routes import web_bp
from aura.application.services.camera_stream_service import CameraStreamService
from aura.application.services.health_service import HealthService
from aura.application.services.robot_control_service import RobotControlService
from aura.application.services.robot_state_store import RobotStateStore
from aura.application.services.robot_status_service import RobotStatusService
from aura.application.services.sensor_service import SensorService
from aura.config.settings import Settings
from aura.infrastructure.actuators.servo_controller import ServoController
from aura.infrastructure.camera.mock_camera import MockCamera
from aura.infrastructure.camera.pi_camera import PiCamera
from aura.infrastructure.communication.mock_transport import MockTransport
from aura.infrastructure.communication.serial_transport import SerialTransport
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
    app.register_blueprint(camera_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(led_bp)
    app.register_blueprint(servo_bp)
    app.register_blueprint(sensor_bp)

    return app


def _build_container(settings: Settings) -> AppContainer:
    camera = _build_camera(settings)
    transport = _build_transport(settings)
    servo_controller = ServoController(transport, settings)
    ultrasonic_sensor = UltrasonicSensorClient(transport)
    state_store = RobotStateStore()
    health_service = HealthService(transport)
    robot_control_service = RobotControlService(
        transport,
        servo_controller,
        state_store,
    )
    return AppContainer(
        camera=camera,
        transport=transport,
        servo_controller=servo_controller,
        state_store=state_store,
        camera_stream_service=CameraStreamService(camera),
        health_service=health_service,
        robot_control_service=robot_control_service,
        robot_status_service=RobotStatusService(state_store, health_service),
        sensor_service=SensorService(ultrasonic_sensor, state_store),
    )


def _build_camera(settings: Settings):
    if settings.camera_provider == "mock":
        return MockCamera()
    return PiCamera(settings)


def _build_transport(settings: Settings):
    if settings.serial_transport == "mock":
        return MockTransport()
    return SerialTransport(settings)
