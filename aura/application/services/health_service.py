from aura.domain.ports.command_transport_port import CommandTransportPort
from aura.infrastructure.communication.protocol import Esp32Protocol


class HealthService:
    def __init__(self, transport: CommandTransportPort):
        self._transport = transport

    def get_health(self) -> dict:
        esp32_response = []
        esp32_status = "ok"
        esp32_error = None

        try:
            esp32_response = self._transport.send(Esp32Protocol.PING)
            if "PONG" not in esp32_response:
                esp32_status = "unknown"
        except Exception as exc:
            esp32_status = "offline"
            esp32_error = str(exc)

        return {
            "status": "ok" if esp32_status == "ok" else "degraded",
            "components": {
                "api": {"status": "ok"},
                "esp32": {
                    "status": esp32_status,
                    "response": esp32_response,
                    "error": esp32_error,
                },
            },
        }
