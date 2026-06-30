#include "UltrasonicSensor.h"

#include "config.h"

void UltrasonicSensor::begin() {
    pinMode(ULTRASONIC_TRIGGER_PIN, OUTPUT);
    pinMode(ULTRASONIC_ECHO_PIN, INPUT);
    digitalWrite(ULTRASONIC_TRIGGER_PIN, LOW);
}

bool UltrasonicSensor::readDistanceCm(float& distanceCm) {
    digitalWrite(ULTRASONIC_TRIGGER_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(ULTRASONIC_TRIGGER_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(ULTRASONIC_TRIGGER_PIN, LOW);

    const unsigned long duration = pulseIn(
        ULTRASONIC_ECHO_PIN,
        HIGH,
        ULTRASONIC_TIMEOUT_US
    );

    if (duration == 0) {
        return false;
    }

    distanceCm = (duration * ULTRASONIC_SOUND_SPEED_CM_PER_US) / 2.0;
    return true;
}
