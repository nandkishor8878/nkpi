from aura.domain.ports.command_transport_port import CommandTransportPort
from aura.application.services.robot_state_store import RobotStateStore
from aura.infrastructure.actuators.servo_controller import ServoController
from aura.infrastructure.communication.protocol import Esp32Protocol


class RobotControlService:
    def __init__(
        self,
        transport: CommandTransportPort,
        servo_controller: ServoController | None = None,
        state_store: RobotStateStore | None = None,
    ):
        self._transport = transport
        self._servo_controller = servo_controller
        self._state_store = state_store

    def turn_led_on(self) -> list[str]:
        response = self._transport.send(Esp32Protocol.LED_ON)
        if self._command_succeeded(response) and self._state_store is not None:
            self._state_store.set_led("on")
        return response

    def turn_led_off(self) -> list[str]:
        response = self._transport.send(Esp32Protocol.LED_OFF)
        if self._command_succeeded(response) and self._state_store is not None:
            self._state_store.set_led("off")
        return response

    def set_servo_angle(self, servo_id: int, angle: int) -> list[str]:
        if self._servo_controller is None:
            raise RuntimeError("Servo controller is not configured")
        response = self._servo_controller.set_angle(servo_id, angle)
        if self._command_succeeded(response) and self._state_store is not None:
            self._state_store.set_servo_angle(servo_id, angle)
        return response

    def _command_succeeded(self, response: list[str]) -> bool:
        return "OK" in response
