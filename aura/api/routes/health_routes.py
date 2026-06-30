from flask import Blueprint, jsonify

from aura.api.routes._container import get_container


health_bp = Blueprint("health", __name__, url_prefix="/api/v1")


@health_bp.get("/health")
def health():
    container = get_container()
    return jsonify(container.health_service.get_health())

