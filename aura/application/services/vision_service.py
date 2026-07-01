from aura.application.services.camera_stream_service import CameraStreamService
from aura.application.services.robot_state_store import RobotStateStore
from aura.config.settings import Settings


class VisionService:
    def __init__(
        self,
        camera_stream_service: CameraStreamService,
        state_store: RobotStateStore,
        settings: Settings | None = None,
    ):
        self._camera_stream_service = camera_stream_service
        self._state_store = state_store
        self._settings = settings or Settings()

    def analyze_frame(self) -> dict:
        frame_bytes = self._camera_stream_service.get_jpeg_frame()
        result = self._analyze_jpeg(frame_bytes)
        self._state_store.set_vision(result)
        return result

    def _analyze_jpeg(self, frame_bytes: bytes) -> dict:
        import cv2
        import numpy as np

        encoded = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
        if frame is None:
            return self._empty_result("frame_decode_failed")

        frame_height, frame_width = frame.shape[:2]
        faces = self._detect_faces(cv2, frame)
        qr_codes = self._detect_qr_codes(cv2, frame)

        return {
            "status": "ok",
            "frame_width": int(frame_width),
            "frame_height": int(frame_height),
            "face_count": len(faces),
            "faces": faces,
            "qr_count": len(qr_codes),
            "qr_codes": qr_codes,
        }

    def _detect_faces(self, cv2, frame) -> list[dict]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)

        cascade_names = [
            "haarcascade_frontalface_default.xml",
            "haarcascade_frontalface_alt2.xml",
        ]
        faces = []
        for cascade_name in cascade_names:
            cascade_path = cv2.data.haarcascades + cascade_name
            detector = cv2.CascadeClassifier(cascade_path)
            if detector.empty():
                continue

            detected = detector.detectMultiScale(
                gray,
                scaleFactor=self._settings.vision_face_scale_factor,
                minNeighbors=self._settings.vision_face_min_neighbors,
                minSize=(
                    self._settings.vision_face_min_size_px,
                    self._settings.vision_face_min_size_px,
                ),
                flags=cv2.CASCADE_SCALE_IMAGE,
            )
            faces.extend(detected)

        faces = self._dedupe_faces(faces)
        return [
            {
                "x": int(x),
                "y": int(y),
                "width": int(width),
                "height": int(height),
            }
            for x, y, width, height in faces
        ]

    def _dedupe_faces(self, faces) -> list[tuple[int, int, int, int]]:
        unique_faces: list[tuple[int, int, int, int]] = []
        for face in sorted(faces, key=lambda item: item[2] * item[3], reverse=True):
            candidate = tuple(int(value) for value in face)
            if all(self._overlap_ratio(candidate, existing) < 0.35 for existing in unique_faces):
                unique_faces.append(candidate)
        return unique_faces

    def _overlap_ratio(
        self,
        first: tuple[int, int, int, int],
        second: tuple[int, int, int, int],
    ) -> float:
        first_x, first_y, first_width, first_height = first
        second_x, second_y, second_width, second_height = second

        left = max(first_x, second_x)
        top = max(first_y, second_y)
        right = min(first_x + first_width, second_x + second_width)
        bottom = min(first_y + first_height, second_y + second_height)
        if right <= left or bottom <= top:
            return 0.0

        intersection = (right - left) * (bottom - top)
        smaller_area = min(first_width * first_height, second_width * second_height)
        return intersection / smaller_area

    def _detect_qr_codes(self, cv2, frame) -> list[dict]:
        detector = cv2.QRCodeDetector()
        ok, decoded_info, points, _ = detector.detectAndDecodeMulti(frame)
        if not ok or points is None:
            return []

        qr_codes = []
        for index, text in enumerate(decoded_info):
            if not text:
                continue
            point_set = points[index]
            qr_codes.append(
                {
                    "text": text,
                    "points": [
                        {"x": int(point[0]), "y": int(point[1])}
                        for point in point_set
                    ],
                }
            )
        return qr_codes

    def _empty_result(self, status: str) -> dict:
        return {
            "status": status,
            "frame_width": None,
            "frame_height": None,
            "face_count": 0,
            "faces": [],
            "qr_count": 0,
            "qr_codes": [],
        }
