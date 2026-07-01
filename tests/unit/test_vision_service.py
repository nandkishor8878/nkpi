import importlib.util
import unittest

from aura.application.services.camera_stream_service import CameraStreamService
from aura.application.services.robot_state_store import RobotStateStore
from aura.application.services.vision_service import VisionService


class FakeCamera:
    def get_frame(self):
        return b"\xff\xd8\xff\xd9"

    def close(self):
        return None


CV2_AVAILABLE = importlib.util.find_spec("cv2") is not None


@unittest.skipUnless(CV2_AVAILABLE, "OpenCV is not installed")
class VisionServiceTests(unittest.TestCase):
    def test_invalid_mock_frame_returns_empty_result_and_updates_state(self):
        state_store = RobotStateStore()
        camera_service = CameraStreamService(FakeCamera())
        service = VisionService(camera_service, state_store)

        result = service.analyze_frame()

        self.assertEqual(result["status"], "frame_decode_failed")
        self.assertEqual(result["face_count"], 0)
        self.assertEqual(result["qr_count"], 0)
        self.assertEqual(state_store.snapshot().vision["status"], "frame_decode_failed")


if __name__ == "__main__":
    unittest.main()
