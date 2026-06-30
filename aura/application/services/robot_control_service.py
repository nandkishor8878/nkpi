from aura.domain.ports.command_transport_port import CommandTransportPort
from aura.infrastructure.actuators.servo_controller import ServoController
from aura.infrastructure.communication.protocol import Esp32Protocol


class RobotControlService:
    def __init__(
        self,
        transport: CommandTransportPort,
        servo_controller: ServoController | None = None,
    ):
        self._transport = transport
        self._servo_controller = servo_controller

    def turn_led_on(self) -> list[str]:
        return self._transport.send(Esp32Protocol.LED_ON)

    def turn_led_off(self) -> list[str]:
        return self._transport.send(Esp32Protocol.LED_OFF)

    def set_servo_angle(self, servo_id: int, angle: int) -> list[str]:
        if self._servo_controller is None:
            raise RuntimeError("Servo controller is not configured")
        return self._servo_controller.set_angle(servo_id, angle)
