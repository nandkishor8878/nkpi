class Esp32Protocol:
    PING = "PING"
    LED_ON = "LED_ON"
    LED_OFF = "LED_OFF"
    READ_DISTANCE = "READ:DISTANCE"
    READ_IMU = "READ:IMU"
    READ_IMU_STATUS = "READ:IMU_STATUS"

    @staticmethod
    def servo_angle(servo_id: int, angle: int) -> str:
        return f"SERVO:{servo_id}:{angle}"
