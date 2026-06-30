#pragma once

#include <Arduino.h>

constexpr uint32_t SERIAL_BAUD_RATE = 115200;
constexpr uint8_t STATUS_LED_PIN = 2;

constexpr uint8_t AURA_PCA9685_I2C_ADDRESS = 0x40;
constexpr uint16_t SERVO_PWM_FREQUENCY = 50;
constexpr uint8_t SERVO_MIN_ANGLE = 0;
constexpr uint8_t SERVO_MAX_ANGLE = 180;
constexpr uint16_t SERVO_MIN_PULSE_US = 500;
constexpr uint16_t SERVO_MAX_PULSE_US = 2500;
constexpr uint8_t SERVO_CHANNEL_COUNT = 16;

constexpr uint8_t ULTRASONIC_TRIGGER_PIN = 5;
constexpr uint8_t ULTRASONIC_ECHO_PIN = 18;
constexpr uint32_t ULTRASONIC_TIMEOUT_US = 30000;
constexpr float ULTRASONIC_SOUND_SPEED_CM_PER_US = 0.0343;
