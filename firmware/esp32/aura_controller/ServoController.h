#pragma once

#include <Adafruit_PWMServoDriver.h>
#include <Arduino.h>

#include "config.h"

class ServoController {
public:
    void begin();
    bool setAngle(uint8_t channel, uint8_t angle);

private:
    Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(AURA_PCA9685_I2C_ADDRESS);

    uint16_t angleToPulse(uint8_t angle) const;
    uint16_t pulseToTicks(uint16_t pulseMicros) const;
    bool isValidChannel(uint8_t channel) const;
    bool isValidAngle(uint8_t angle) const;
};
