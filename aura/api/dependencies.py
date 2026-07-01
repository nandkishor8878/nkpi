from dataclasses import dataclass

from aura.application.services.camera_stream_service import CameraStreamService
from aura.application.services.health_service import HealthService
from aura.application.services.robot_control_service import RobotControlService
from aura.application.services.robot_state_store import RobotStateStore
from aura.application.services.robot_status_service import RobotStatusService
from aura.application.services.servo_service import ServoService
from aura.application.services.sensor_service import SensorService
from aura.domain.ports.camera_port import CameraPort
from aura.domain.ports.command_transport_port import CommandTransportPort
from aura.infrastructure.actuators.servo_controller import ServoController


@dataclass
class AppContainer:
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

    def close(self) -> None:
        self.camera.close()
        self.transport.close()
