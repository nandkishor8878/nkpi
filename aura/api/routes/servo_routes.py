from flask import Blueprint, jsonify, request

from aura.api.routes._container import get_container


servo_bp = Blueprint("servo", __name__, url_prefix="/api/v1")


@servo_bp.post("/servos/<int:servo_id>/angle")
def set_servo_angle(servo_id: int):
    payload = request.get_json(silent=True) or {}
    angle = payload.get("angle")

    if type(angle) is not int:
        return jsonify({"status": "error", "error": "angle must be an integer"}), 400

    container = get_container()
    try:
        response = container.robot_control_service.set_servo_angle(servo_id, angle)
    except ValueError as exc:
        return jsonify({"status": "error", "error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"status": "error", "error": str(exc)}), 503

    return jsonify(
        {
            "status": "success",
            "servo_id": servo_id,
            "angle": angle,
            "response": response,
        }
    )
