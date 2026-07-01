from flask import Blueprint, jsonify

from aura.api.routes._container import get_container


vision_bp = Blueprint("vision", __name__, url_prefix="/api/v1")


@vision_bp.get("/vision/analyze")
def analyze_vision():
    container = get_container()

    try:
        result = container.vision_service.analyze_frame()
    except Exception as exc:
        container.state_store.record_error(f"Vision scan failed: {exc}")
        return jsonify({"status": "error", "error": str(exc)}), 503

    return jsonify(
        {
            "status": "success",
            "vision": result,
        }
    )
