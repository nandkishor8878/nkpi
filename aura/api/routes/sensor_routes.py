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


@sensor_bp.get("/sensors/proximity")
def read_proximity():
    container = get_container()

    try:
        proximity = container.sensor_service.read_proximity()
    except Exception as exc:
        return jsonify({"status": "error", "error": str(exc)}), 503

    return jsonify(
        {
            "status": "success",
            "proximity": proximity,
        }
    )


@sensor_bp.get("/sensors/imu")
def read_imu():
    container = get_container()

    try:
        imu = container.sensor_service.read_imu()
    except Exception as exc:
        return jsonify({"status": "error", "error": str(exc)}), 503

    return jsonify(
        {
            "status": "success",
            "imu": imu,
        }
    )
