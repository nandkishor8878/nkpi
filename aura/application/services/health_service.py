from aura.domain.ports.command_transport_port import CommandTransportPort
from aura.infrastructure.communication.protocol import Esp32Protocol


class HealthService:
    def __init__(self, transport: CommandTransportPort):
        self._transport = transport

    def get_health(self) -> dict:
        esp32_response = self._transport.send(Esp32Protocol.PING)
        return {
            "status": "ok",
            "components": {
                "api": {"status": "ok"},
                "esp32": {
                    "status": "ok" if "PONG" in esp32_response else "unknown",
                    "response": esp32_response,
                },
            },
        }

