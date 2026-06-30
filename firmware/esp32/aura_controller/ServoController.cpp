#include "ServoController.h"

#include "config.h"

void ServoController::begin() {
    pwm.begin();
    pwm.setPWMFreq(SERVO_PWM_FREQUENCY);
}

bool ServoController::setAngle(uint8_t channel, uint8_t angle) {
    if (!isValidChannel(channel) || !isValidAngle(angle)) {
        return false;
    }

    const uint16_t pulseMicros = angleToPulse(angle);
    const uint16_t ticks = pulseToTicks(pulseMicros);
    pwm.setPWM(channel, 0, ticks);
    return true;
}

uint16_t ServoController::angleToPulse(uint8_t angle) const {
    return map(
        angle,
        SERVO_MIN_ANGLE,
        SERVO_MAX_ANGLE,
        SERVO_MIN_PULSE_US,
        SERVO_MAX_PULSE_US
    );
}

uint16_t ServoController::pulseToTicks(uint16_t pulseMicros) const {
    const uint32_t periodMicros = 1000000UL / SERVO_PWM_FREQUENCY;
    return static_cast<uint16_t>((static_cast<uint32_t>(pulseMicros) * 4096UL) / periodMicros);
}

bool ServoController::isValidChannel(uint8_t channel) const {
    return channel < SERVO_CHANNEL_COUNT;
}

bool ServoController::isValidAngle(uint8_t angle) const {
    return angle >= SERVO_MIN_ANGLE && angle <= SERVO_MAX_ANGLE;
}
