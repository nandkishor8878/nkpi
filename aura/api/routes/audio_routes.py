from flask import Blueprint, jsonify, request

from aura.api.routes._container import get_container


audio_bp = Blueprint("audio", __name__, url_prefix="/api/v1")


@audio_bp.get("/audio/status")
def get_audio_status():
    container = get_container()
    return jsonify(
        {
            "status": "success",
            "audio": container.audio_service.status(),
        }
    )


@audio_bp.post("/audio/record")
def record_audio():
    payload = request.get_json(silent=True) or {}
    duration_seconds = payload.get("duration_seconds")

    container = get_container()
    try:
        result = container.audio_service.record(duration_seconds)
    except ValueError as exc:
        return jsonify({"status": "error", "error": str(exc)}), 400
    except Exception as exc:
        container.state_store.record_error(f"Audio record failed: {exc}")
        return jsonify({"status": "error", "error": str(exc)}), 503

    return jsonify({"status": "success", "audio": result})
