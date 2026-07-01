import logging

from aura.application.services.robot_state_store import RobotStateStore
from aura.application.services.servo_service import ServoService
from aura.application.services.vision_service import VisionService
from aura.config.settings import Settings


logger = logging.getLogger(__name__)


class FaceTrackingService:
    def __init__(
        self,
        vision_service: VisionService,
        servo_service: ServoService,
        state_store: RobotStateStore,
        settings: Settings,
    ):
        self._vision_service = vision_service
        self._servo_service = servo_service
        self._state_store = state_store
        self._settings = settings

    def track_once(self) -> dict:
        vision = self._vision_service.analyze_frame()
        face = self._select_target_face(vision.get("faces", []))
        frame_width = vision.get("frame_width") or self._settings.camera_width
        frame_height = vision.get("frame_height") or self._settings.camera_height

        if face is None:
            result = self._result(
                "no_face",
                vision,
                frame_width,
                frame_height,
                None,
                None,
                None,
            )
            self._state_store.set_face_tracking(result)
            return result

        face_center_x = face["x"] + (face["width"] / 2)
        frame_center_x = frame_width / 2
        error_px = int(round(face_center_x - frame_center_x))

        if abs(error_px) <= self._settings.face_tracking_dead_zone_px:
            result = self._result(
                "centered",
                vision,
                frame_width,
                frame_height,
                face,
                error_px,
                None,
            )
            self._state_store.set_face_tracking(result)
            return result

        channel = self._settings.face_tracking_servo_channel
        current_angle = self._current_angle(channel)
        direction = 1 if error_px > 0 else -1
        if self._settings.face_tracking_invert_servo:
            direction *= -1

        target_angle = self._clamp_angle(
            current_angle + direction * self._settings.face_tracking_step_degrees
        )

        if target_angle == current_angle:
            result = self._result(
                "limit_reached",
                vision,
                frame_width,
                frame_height,
                face,
                error_px,
                {
                    "channel": channel,
                    "angle": current_angle,
                    "response": ["LIMIT_REACHED"],
                },
            )
            self._state_store.set_face_tracking(result)
            return result

        try:
            servo = self._servo_service.set_angle(
                channel,
                target_angle,
                smooth=self._settings.face_tracking_smooth,
            )
        except Exception:
            self._state_store.record_error("Face tracking servo move failed")
            logger.exception("Face tracking failed while moving servo")
            raise

        result = self._result(
            "moved",
            vision,
            frame_width,
            frame_height,
            face,
            error_px,
            servo,
        )
        self._state_store.set_face_tracking(result)
        return result

    def status(self) -> dict:
        state = self._state_store.snapshot()
        return state.face_tracking or {
            "status": "idle",
            "servo_channel": self._settings.face_tracking_servo_channel,
            "dead_zone_px": self._settings.face_tracking_dead_zone_px,
            "step_degrees": self._settings.face_tracking_step_degrees,
            "invert_servo": self._settings.face_tracking_invert_servo,
        }

    def _select_target_face(self, faces: list[dict]) -> dict | None:
        if not faces:
            return None
        return max(faces, key=lambda face: face["width"] * face["height"])

    def _current_angle(self, channel: int) -> int:
        angle = self._state_store.snapshot().servos.get(channel)
        if isinstance(angle, int):
            return angle
        return self._settings.servo_center_angle

    def _clamp_angle(self, angle: int) -> int:
        return max(
            self._settings.servo_min_angle,
            min(self._settings.servo_max_angle, angle),
        )

    def _result(
        self,
        status: str,
        vision: dict,
        frame_width: int,
        frame_height: int,
        face: dict | None,
        error_px: int | None,
        servo: dict | None,
    ) -> dict:
        return {
            "status": status,
            "servo_channel": self._settings.face_tracking_servo_channel,
            "dead_zone_px": self._settings.face_tracking_dead_zone_px,
            "step_degrees": self._settings.face_tracking_step_degrees,
            "frame_width": frame_width,
            "frame_height": frame_height,
            "target_face": face,
            "error_px": error_px,
            "servo": servo,
            "vision": {
                "status": vision.get("status"),
                "face_count": vision.get("face_count", 0),
                "qr_count": vision.get("qr_count", 0),
            },
        }
