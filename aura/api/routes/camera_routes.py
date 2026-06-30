from flask import Blueprint, Response

from aura.api.routes._container import get_container


camera_bp = Blueprint("camera", __name__)


@camera_bp.get("/api/v1/camera/stream")
@camera_bp.get("/video")
def video_stream():
    container = get_container()
    return Response(
        container.camera_stream_service.mjpeg_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )

