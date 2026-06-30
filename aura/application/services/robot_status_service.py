from aura.application.services.health_service import HealthService
from aura.application.services.robot_state_store import RobotStateStore


class RobotStatusService:
    def __init__(self, state_store: RobotStateStore, health_service: HealthService):
        self._state_store = state_store
        self._health_service = health_service

    def get_status(self) -> dict:
        state = self._state_store.snapshot()
        health = self._health_service.get_health()

        return {
            "status": "online",
            "robot": {
                "name": "Aura",
                "mode": state.mode,
                "uptime_seconds": state.uptime_seconds(),
            },
            "components": {
                "api": health["components"]["api"]["status"],
                "camera": "ok",
                "esp32": health["components"]["esp32"]["status"],
                "servo": "ready",
            },
            "actuators": {
                "led": state.led,
                "servos": {
                    str(servo_id): {"angle": angle}
                    for servo_id, angle in sorted(state.servos.items())
                },
            },
            "sensors": {
                "distance_cm": state.distance_cm,
                "imu": state.imu,
            },
            "visitor": state.visitor,
        }
