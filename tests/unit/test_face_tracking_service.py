import unittest

from aura.application.services.face_tracking_service import FaceTrackingService
from aura.application.services.robot_state_store import RobotStateStore
from aura.config.settings import Settings


class FakeVisionService:
    def __init__(self, result):
        self._result = result

    def analyze_frame(self):
        return self._result


class FakeServoService:
    def __init__(self):
        self.moves = []

    def set_angle(self, channel, angle, smooth=True):
        move = {"channel": channel, "angle": angle, "smooth": smooth}
        self.moves.append(move)
        return move


def vision_result(faces):
    return {
        "status": "ok",
        "frame_width": 640,
        "frame_height": 480,
        "face_count": len(faces),
        "faces": faces,
        "qr_count": 0,
        "qr_codes": [],
    }


class FaceTrackingServiceTests(unittest.TestCase):
    def test_no_face_does_not_move_servo(self):
        state_store = RobotStateStore()
        servo = FakeServoService()
        service = FaceTrackingService(
            FakeVisionService(vision_result([])),
            servo,
            state_store,
            Settings(face_tracking_dead_zone_px=50),
        )

        result = service.track_once()

        self.assertEqual(result["status"], "no_face")
        self.assertEqual(servo.moves, [])
        self.assertEqual(state_store.snapshot().face_tracking["status"], "no_face")

    def test_centered_face_does_not_move_servo(self):
        state_store = RobotStateStore()
        servo = FakeServoService()
        service = FaceTrackingService(
            FakeVisionService(vision_result([{"x": 300, "y": 80, "width": 40, "height": 40}])),
            servo,
            state_store,
            Settings(face_tracking_dead_zone_px=50),
        )

        result = service.track_once()

        self.assertEqual(result["status"], "centered")
        self.assertEqual(result["error_px"], 0)
        self.assertEqual(servo.moves, [])

    def test_face_on_right_moves_servo_positive_step(self):
        state_store = RobotStateStore()
        state_store.set_servo_angle(0, 90)
        servo = FakeServoService()
        service = FaceTrackingService(
            FakeVisionService(vision_result([{"x": 500, "y": 80, "width": 60, "height": 60}])),
            servo,
            state_store,
            Settings(face_tracking_dead_zone_px=20, face_tracking_step_degrees=5),
        )

        result = service.track_once()

        self.assertEqual(result["status"], "moved")
        self.assertEqual(servo.moves[-1]["angle"], 95)

    def test_face_on_left_moves_servo_negative_step(self):
        state_store = RobotStateStore()
        state_store.set_servo_angle(0, 90)
        servo = FakeServoService()
        service = FaceTrackingService(
            FakeVisionService(vision_result([{"x": 80, "y": 80, "width": 60, "height": 60}])),
            servo,
            state_store,
            Settings(face_tracking_dead_zone_px=20, face_tracking_step_degrees=5),
        )

        result = service.track_once()

        self.assertEqual(result["status"], "moved")
        self.assertEqual(servo.moves[-1]["angle"], 85)

    def test_tracking_does_not_move_beyond_angle_limits(self):
        state_store = RobotStateStore()
        state_store.set_servo_angle(0, 150)
        servo = FakeServoService()
        service = FaceTrackingService(
            FakeVisionService(vision_result([{"x": 500, "y": 80, "width": 60, "height": 60}])),
            servo,
            state_store,
            Settings(
                servo_max_angle=150,
                face_tracking_dead_zone_px=20,
                face_tracking_step_degrees=5,
            ),
        )

        result = service.track_once()

        self.assertEqual(result["status"], "limit_reached")
        self.assertEqual(servo.moves, [])


if __name__ == "__main__":
    unittest.main()
