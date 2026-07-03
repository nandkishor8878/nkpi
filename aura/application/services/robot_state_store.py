import time

from aura.domain.models.robot_state import DiagnosticEvent, RobotState


MAX_DIAGNOSTIC_EVENTS = 20


class RobotStateStore:
    def __init__(self):
        self._state = RobotState()

    def set_led(self, state: str) -> None:
        self._state.led = state
        self.record_command(f"LED {state}")

    def set_servo_angle(self, servo_id: int, angle: int) -> None:
        self._state.servos[servo_id] = angle
        self.record_command(f"Servo {servo_id} angle {angle}")

    def stop_servo(self, servo_id: int) -> None:
        self._state.servos[servo_id] = None
        self.record_command(f"Servo {servo_id} stop")

    def set_distance_cm(self, distance_cm: float) -> None:
        self._state.distance_cm = distance_cm
        self.record_command(f"Distance {distance_cm:.1f} cm")

    def set_proximity(self, detected: bool, distance_cm: float) -> None:
        self._state.proximity_detected = detected
        self._state.distance_cm = distance_cm
        state = "detected" if detected else "clear"
        self.record_command(f"Proximity {state} at {distance_cm:.1f} cm")

    def set_imu(self, imu: dict) -> None:
        self._state.imu = imu
        self.record_command("IMU read")

    def set_vision(self, vision: dict) -> None:
        self._state.vision = vision
        face_count = vision.get("face_count", 0)
        qr_count = vision.get("qr_count", 0)
        if self._state.visitor_state is None:
            self._state.visitor = "Detected" if face_count else None
        self.record_command(f"Vision scan faces={face_count} qr={qr_count}")

    def set_face_tracking(self, tracking: dict) -> None:
        self._state.face_tracking = tracking
        self.record_command(f"Face tracking {tracking.get('status', 'unknown')}")

    def set_visitor_state(self, visitor_state: dict) -> None:
        self._state.visitor_state = visitor_state
        self._state.visitor = visitor_state.get("display")
        self.record_command(f"Visitor {visitor_state.get('state', 'unknown')}")

    def set_speech(self, speech: dict) -> None:
        self._state.speech = speech
        self.record_command(f"Speech {speech.get('status', 'unknown')}")

    def set_audio(self, audio: dict) -> None:
        self._state.audio = audio
        self.record_command(f"Audio {audio.get('status', 'unknown')}")

    def set_speech_recognition(self, recognition: dict) -> None:
        self._state.speech_recognition = recognition
        self.record_command(f"Speech recognition {recognition.get('status', 'unknown')}")

    def set_visitor_transcript(self, transcript: str, recognition: dict) -> None:
        visitor_state = self._state.visitor_state or {
            "state": "waiting_for_response",
            "display": "Waiting for response",
        }
        visitor_state = {
            **visitor_state,
            "state": "waiting_for_response",
            "display": "Waiting for response",
            "latest_transcript": transcript,
            "speech_recognition": recognition,
        }
        self._state.visitor_state = visitor_state
        self._state.visitor = visitor_state.get("display")
        self.record_command("Visitor transcript updated")

    def record_command(self, message: str) -> None:
        self._state.command_count += 1
        self._state.last_command = message
        self._append_event("info", message)

    def record_error(self, message: str) -> None:
        self._state.error_count += 1
        self._state.last_error = message
        self._append_event("error", message)

    def _append_event(self, level: str, message: str) -> None:
        self._state.events.append(
            DiagnosticEvent(
                timestamp=time.time(),
                level=level,
                message=message,
            )
        )
        self._state.events = self._state.events[-MAX_DIAGNOSTIC_EVENTS:]

    def snapshot(self) -> RobotState:
        return self._state
