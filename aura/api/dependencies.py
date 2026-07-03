from dataclasses import dataclass

from aura.application.services.audio_service import AudioService
from aura.application.services.camera_stream_service import CameraStreamService
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
from aura.domain.ports.camera_port import CameraPort
from aura.domain.ports.command_transport_port import CommandTransportPort
from aura.infrastructure.actuators.servo_controller import ServoController


@dataclass
class AppContainer:
    settings: Settings
    camera: CameraPort
    transport: CommandTransportPort
    servo_controller: ServoController
    state_store: RobotStateStore
    camera_stream_service: CameraStreamService
    health_service: HealthService
    robot_control_service: RobotControlService
    servo_service: ServoService
    robot_status_service: RobotStatusService
    sensor_service: SensorService
    audio_service: AudioService
    speech_service: SpeechService
    speech_recognition_service: SpeechRecognitionService
    vision_service: VisionService
    face_tracking_service: FaceTrackingService
    visitor_service: VisitorService

    def close(self) -> None:
        self.camera.close()
        self.transport.close()
