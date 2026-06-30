class Esp32Protocol:
    PING = "PING"
    LED_ON = "LED_ON"
    LED_OFF = "LED_OFF"
    READ_DISTANCE = "READ:DISTANCE"

    @staticmethod
    def servo_angle(servo_id: int, angle: int) -> str:
        return f"SERVO:{servo_id}:{angle}"
