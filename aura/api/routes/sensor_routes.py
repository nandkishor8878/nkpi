from flask import Blueprint, jsonify

from aura.api.routes._container import get_container


sensor_bp = Blueprint("sensor", __name__, url_prefix="/api/v1")


@sensor_bp.get("/sensors/distance")
def read_distance():
    container = get_container()

    try:
        distance_cm = container.sensor_service.read_distance_cm()
    except Exception as exc:
        return jsonify({"status": "error", "error": str(exc)}), 503

    return jsonify(
        {
            "status": "success",
            "distance_cm": distance_cm,
        }
    )
