from flask import Blueprint, jsonify

from aura.api.routes._container import get_container


face_tracking_bp = Blueprint("face_tracking", __name__, url_prefix="/api/v1")


@face_tracking_bp.get("/face-tracking/status")
def get_face_tracking_status():
    container = get_container()
    return jsonify(
        {
            "status": "success",
            "face_tracking": container.face_tracking_service.status(),
        }
    )


@face_tracking_bp.post("/face-tracking/track")
def track_face_once():
    container = get_container()

    try:
        result = container.face_tracking_service.track_once()
    except Exception as exc:
        container.state_store.record_error(f"Face tracking failed: {exc}")
        return jsonify({"status": "error", "error": str(exc)}), 503

    return jsonify(
        {
            "status": "success",
            "face_tracking": result,
        }
    )
