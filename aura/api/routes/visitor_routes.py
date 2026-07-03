from flask import Blueprint, jsonify, request

from aura.api.routes._container import get_container


visitor_bp = Blueprint("visitor", __name__, url_prefix="/api/v1")


@visitor_bp.get("/visitor/status")
def get_visitor_status():
    container = get_container()
    return jsonify(
        {
            "status": "success",
            "visitor": container.visitor_service.status(),
        }
    )


@visitor_bp.post("/visitor/check")
def check_visitor():
    payload = request.get_json(silent=True) or {}
    track = payload.get("track", True)

    if type(track) is not bool:
        return jsonify({"status": "error", "error": "track must be a boolean"}), 400

    container = get_container()
    try:
        visitor = container.visitor_service.check_visitor(track=track)
    except Exception as exc:
        container.state_store.record_error(f"Visitor check failed: {exc}")
        return jsonify({"status": "error", "error": str(exc)}), 503

    return jsonify({"status": "success", "visitor": visitor})


@visitor_bp.post("/visitor/reset")
def reset_visitor():
    container = get_container()
    return jsonify(
        {
            "status": "success",
            "visitor": container.visitor_service.reset(),
        }
    )
