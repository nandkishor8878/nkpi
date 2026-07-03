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
                    str(servo_id): {
                        "angle": angle,
                        "state": "stopped" if angle is None else "positioned",
                    }
                    for servo_id, angle in sorted(state.servos.items())
                },
            },
            "sensors": {
                "distance_cm": state.distance_cm,
                "proximity_detected": state.proximity_detected,
                "imu": state.imu,
            },
            "vision": state.vision,
            "face_tracking": state.face_tracking,
            "visitor_state": state.visitor_state,
            "visitor": state.visitor,
            "speech": state.speech,
            "audio": state.audio,
            "speech_recognition": state.speech_recognition,
            "diagnostics": {
                "command_count": state.command_count,
                "error_count": state.error_count,
                "last_command": state.last_command,
                "last_error": state.last_error,
                "recent_events": [
                    {
                        "timestamp": event.timestamp,
                        "level": event.level,
                        "message": event.message,
                    }
                    for event in state.events[-8:]
                ],
            },
        }
