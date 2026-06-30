from aura.domain.ports.command_transport_port import CommandTransportPort
from aura.infrastructure.communication.protocol import Esp32Protocol


class UltrasonicSensorClient:
    def __init__(self, transport: CommandTransportPort):
        self._transport = transport

    def read_distance_cm(self) -> float:
        response = self._transport.send(Esp32Protocol.READ_DISTANCE)
        return self._parse_distance_response(response)

    def _parse_distance_response(self, response: list[str]) -> float:
        for line in response:
            if line.startswith("DISTANCE_CM:"):
                return float(line.split(":", 1)[1])

        error = next((line for line in response if line.startswith("ERROR:")), None)
        if error is not None:
            raise RuntimeError(error)

        raise RuntimeError("Distance response missing DISTANCE_CM value")
