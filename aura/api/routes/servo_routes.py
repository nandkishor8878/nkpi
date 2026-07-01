from flask import Blueprint, jsonify, request

from aura.api.routes._container import get_container


servo_bp = Blueprint("servo", __name__, url_prefix="/api/v1")


@servo_bp.post("/servo")
def set_servo():
    payload = request.get_json(silent=True) or {}
    channel = payload.get("channel")
    angle = payload.get("angle")
    smooth = payload.get("smooth", True)

    if channel is not None and type(channel) is not int:
        return jsonify({"status": "error", "error": "channel must be an integer"}), 400
    if type(angle) is not int:
        return jsonify({"status": "error", "error": "angle must be an integer"}), 400
    if type(smooth) is not bool:
        return jsonify({"status": "error", "error": "smooth must be a boolean"}), 400

    container = get_container()
    try:
        result = container.servo_service.set_angle(channel, angle, smooth)
    except ValueError as exc:
        return jsonify({"status": "error", "error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"status": "error", "error": str(exc)}), 503

    return jsonify({"status": "success", **result})


@servo_bp.post("/servo/stop")
def stop_servo():
    payload = request.get_json(silent=True) or {}
    channel = payload.get("channel")

    if channel is not None and type(channel) is not int:
        return jsonify({"status": "error", "error": "channel must be an integer"}), 400

    container = get_container()
    try:
        result = container.servo_service.stop(channel)
    except ValueError as exc:
        return jsonify({"status": "error", "error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"status": "error", "error": str(exc)}), 503

    return jsonify({"status": "success", **result})


@servo_bp.post("/servos/<int:servo_id>/angle")
def set_servo_angle(servo_id: int):
    payload = request.get_json(silent=True) or {}
    angle = payload.get("angle")

    if type(angle) is not int:
        return jsonify({"status": "error", "error": "angle must be an integer"}), 400

    container = get_container()
    try:
        result = container.servo_service.set_angle(servo_id, angle)
    except ValueError as exc:
        return jsonify({"status": "error", "error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"status": "error", "error": str(exc)}), 503

    return jsonify(
        {
            "status": "success",
            "servo_id": result["channel"],
            "channel": result["channel"],
            "angle": result["angle"],
            "response": result["response"],
        }
    )
