from aura.domain.ports.command_transport_port import CommandTransportPort
from aura.infrastructure.communication.protocol import Esp32Protocol


class ImuSensorClient:
    _FIELDS = {
        "AX": "accel_x",
        "AY": "accel_y",
        "AZ": "accel_z",
        "GX": "gyro_x",
        "GY": "gyro_y",
        "GZ": "gyro_z",
    }

    def __init__(self, transport: CommandTransportPort):
        self._transport = transport

    def read_imu(self) -> dict:
        response = self._transport.send(Esp32Protocol.READ_IMU)
        return self._parse_imu_response(response)

    def read_status(self) -> dict:
        response = self._transport.send(Esp32Protocol.READ_IMU_STATUS)
        return self._parse_status_response(response)

    def _parse_imu_response(self, response: list[str]) -> dict:
        for line in response:
            if line.startswith("IMU:"):
                return self._parse_imu_line(line)

        error = next((line for line in response if line.startswith("ERROR:")), None)
        if error is not None:
            raise RuntimeError(error)

        raise RuntimeError("IMU response missing IMU value")

    def _parse_status_response(self, response: list[str]) -> dict:
        for line in response:
            if line.startswith("IMU_STATUS:"):
                return self._parse_status_line(line)

        error = next((line for line in response if line.startswith("ERROR:")), None)
        if error is not None:
            raise RuntimeError(error)

        raise RuntimeError("IMU status response missing IMU_STATUS value")

    def _parse_status_line(self, line: str) -> dict:
        parts = line.split(":")
        if len(parts) != 7 or parts[0] != "IMU_STATUS":
            raise RuntimeError("Invalid IMU status response format")

        values = {}
        for index in range(1, len(parts), 2):
            values[parts[index]] = parts[index + 1]

        return {
            "connected": values.get("CONNECTED") == "1",
            "address": values.get("ADDRESS"),
            "error": values.get("ERROR"),
        }

    def _parse_imu_line(self, line: str) -> dict:
        parts = line.split(":")
        if len(parts) != 13 or parts[0] != "IMU":
            raise RuntimeError("Invalid IMU response format")

        parsed = {}
        for index in range(1, len(parts), 2):
            label = parts[index]
            value = parts[index + 1]
            field_name = self._FIELDS.get(label)
            if field_name is None:
                raise RuntimeError(f"Unknown IMU field: {label}")
            parsed[field_name] = float(value)

        missing_fields = set(self._FIELDS.values()) - set(parsed)
        if missing_fields:
            raise RuntimeError("IMU response missing required fields")

        return parsed
