from aura.config.settings import Settings
from aura.domain.ports.command_transport_port import CommandTransportPort
from aura.infrastructure.communication.protocol import Esp32Protocol


class ServoController:
    def __init__(self, transport: CommandTransportPort, settings: Settings):
        self._transport = transport
        self._min_angle = settings.servo_min_angle
        self._max_angle = settings.servo_max_angle

    def set_angle(self, servo_id: int, angle: int) -> list[str]:
        self._validate_servo_id(servo_id)
        self._validate_angle(angle)
        return self._transport.send(Esp32Protocol.servo_angle(servo_id, angle))

    def _validate_servo_id(self, servo_id: int) -> None:
        if servo_id < 0:
            raise ValueError("servo_id must be greater than or equal to 0")

    def _validate_angle(self, angle: int) -> None:
        if angle < self._min_angle or angle > self._max_angle:
            raise ValueError(
                f"angle must be between {self._min_angle} and {self._max_angle}"
            )
