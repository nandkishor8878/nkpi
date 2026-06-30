from flask import Blueprint, jsonify

from aura.api.routes._container import get_container


led_bp = Blueprint("led", __name__, url_prefix="/api/v1")


@led_bp.post("/led/on")
def led_on():
    container = get_container()
    response = container.robot_control_service.turn_led_on()
    return jsonify({"status": "success", "response": response})


@led_bp.post("/led/off")
def led_off():
    container = get_container()
    response = container.robot_control_service.turn_led_off()
    return jsonify({"status": "success", "response": response})

