import time

from aura.application.services.face_tracking_service import FaceTrackingService
from aura.application.services.robot_state_store import RobotStateStore
from aura.application.services.speech_service import SpeechService
from aura.config.settings import Settings


class VisitorService:
    def __init__(
        self,
        face_tracking_service: FaceTrackingService,
        state_store: RobotStateStore,
        settings: Settings,
        speech_service: SpeechService | None = None,
    ):
        self._face_tracking_service = face_tracking_service
        self._state_store = state_store
        self._settings = settings
        self._speech_service = speech_service

    def check_visitor(self, track: bool = True) -> dict:
        now = time.time()
        tracking = (
            self._face_tracking_service.track_once()
            if track
            else self._state_store.snapshot().face_tracking
        )
        face_count = self._face_count(tracking)
        current = self._current_state()

        if face_count <= 0:
            visitor_state = self._no_visitor_state(now, current, tracking)
            self._state_store.set_visitor_state(visitor_state)
            return visitor_state

        last_greeted_at = current.get("last_greeted_at")
        greeting_count = current.get("greeting_count", 0)
        should_greet = (
            last_greeted_at is None
            or now - last_greeted_at >= self._settings.visitor_greeting_cooldown_seconds
        )

        if should_greet:
            greeting_count += 1
            greeting = self._settings.visitor_greeting_message
            speech = self._speak_greeting(greeting)
            visitor_state = self._state(
                "greeting",
                now,
                tracking,
                last_seen_at=now,
                last_greeted_at=now,
                greeting_count=greeting_count,
                greeting=greeting,
                speech=speech,
            )
        else:
            visitor_state = self._state(
                "waiting_for_response",
                now,
                tracking,
                last_seen_at=now,
                last_greeted_at=last_greeted_at,
                greeting_count=greeting_count,
                greeting=None,
                speech=None,
            )

        self._state_store.set_visitor_state(visitor_state)
        return visitor_state

    def status(self) -> dict:
        now = time.time()
        current = self._current_state()
        if current["state"] == "greeting":
            greeted_at = current.get("last_greeted_at") or now
            if now - greeted_at >= self._settings.visitor_greeting_display_seconds:
                current = self._state(
                    "waiting_for_response",
                    now,
                    current.get("tracking"),
                    last_seen_at=current.get("last_seen_at"),
                    last_greeted_at=current.get("last_greeted_at"),
                    greeting_count=current.get("greeting_count", 0),
                    greeting=None,
                    speech=current.get("speech"),
                )
                self._state_store.set_visitor_state(current)
        return current

    def reset(self) -> dict:
        visitor_state = self._state(
            "no_visitor",
            time.time(),
            None,
            last_seen_at=None,
            last_greeted_at=None,
            greeting_count=0,
            greeting=None,
            speech=None,
        )
        self._state_store.set_visitor_state(visitor_state)
        return visitor_state

    def _no_visitor_state(self, now: float, current: dict, tracking: dict | None) -> dict:
        last_seen_at = current.get("last_seen_at")
        recently_seen = (
            isinstance(last_seen_at, (int, float))
            and now - last_seen_at < self._settings.visitor_presence_timeout_seconds
        )
        state = "visitor_detected" if recently_seen else "no_visitor"
        return self._state(
            state,
            now,
            tracking,
            last_seen_at=last_seen_at if recently_seen else None,
            last_greeted_at=current.get("last_greeted_at"),
            greeting_count=current.get("greeting_count", 0),
            greeting=None,
            speech=None,
        )

    def _current_state(self) -> dict:
        state = self._state_store.snapshot().visitor_state
        if state is not None:
            return state
        return self._state(
            "no_visitor",
            time.time(),
            None,
            last_seen_at=None,
            last_greeted_at=None,
            greeting_count=0,
            greeting=None,
            speech=None,
        )

    def _face_count(self, tracking: dict | None) -> int:
        if not tracking:
            return 0
        vision = tracking.get("vision") or {}
        return int(vision.get("face_count", 0) or 0)

    def _state(
        self,
        state: str,
        now: float,
        tracking: dict | None,
        last_seen_at: float | None,
        last_greeted_at: float | None,
        greeting_count: int,
        greeting: str | None,
        speech: dict | None,
    ) -> dict:
        return {
            "state": state,
            "display": self._display(state),
            "greeting": greeting,
            "speech": speech,
            "last_seen_at": last_seen_at,
            "last_greeted_at": last_greeted_at,
            "greeting_count": greeting_count,
            "cooldown_seconds": self._settings.visitor_greeting_cooldown_seconds,
            "updated_at": now,
            "tracking": tracking,
        }

    def _speak_greeting(self, greeting: str) -> dict | None:
        if not self._settings.visitor_speak_greeting or self._speech_service is None:
            return None
        try:
            return self._speech_service.speak(greeting)
        except Exception as exc:
            self._state_store.record_error(f"Visitor greeting speech failed: {exc}")
            return {
                "status": "error",
                "error": str(exc),
            }

    def _display(self, state: str) -> str:
        displays = {
            "no_visitor": "No visitor",
            "visitor_detected": "Visitor detected",
            "greeting": "Greeting",
            "waiting_for_response": "Waiting for response",
        }
        return displays.get(state, state)
