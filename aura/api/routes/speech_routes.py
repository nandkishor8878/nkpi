from flask import Blueprint, jsonify, request

from aura.api.routes._container import get_container


speech_bp = Blueprint("speech", __name__, url_prefix="/api/v1")


@speech_bp.get("/speech/status")
def get_speech_status():
    container = get_container()
    return jsonify(
        {
            "status": "success",
            "speech": container.speech_service.status(),
        }
    )


@speech_bp.post("/speech/say")
def say_text():
    container = get_container()
    payload = request.get_json(silent=True) or {}
    text = payload.get("text") or container.visitor_service.status().get("greeting")
    if text is None:
        text = container.settings.visitor_greeting_message

    try:
        result = container.speech_service.speak(text)
    except ValueError as exc:
        return jsonify({"status": "error", "error": str(exc)}), 400
    except Exception as exc:
        container.state_store.record_error(f"Speech failed: {exc}")
        return jsonify({"status": "error", "error": str(exc)}), 503

    return jsonify({"status": "success", "speech": result})
