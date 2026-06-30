from aura.config.settings import Settings
from aura.infrastructure.communication.serial_transport import SerialTransport

class SerialService:
    """Compatibility wrapper for older imports.

    New code should depend on SerialTransport through CommandTransportPort.
    """

    def __init__(self, settings: Settings | None = None):
        self._transport = SerialTransport(settings or Settings.from_env())

    def send(self, command: str) -> list[str]:
        return self._transport.send(command)
