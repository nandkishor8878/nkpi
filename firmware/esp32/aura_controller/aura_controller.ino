#include <Arduino.h>
#include <Wire.h>

#include "CommandDispatcher.h"
#include "Mpu6050Sensor.h"
#include "ServoController.h"
#include "UltrasonicSensor.h"
#include "config.h"

ServoController servoController;
UltrasonicSensor ultrasonicSensor;
Mpu6050Sensor imuSensor;
CommandDispatcher commandDispatcher(servoController, ultrasonicSensor, imuSensor);

void setup() {
    pinMode(STATUS_LED_PIN, OUTPUT);
    digitalWrite(STATUS_LED_PIN, LOW);

    Serial.begin(SERIAL_BAUD_RATE);
    Wire.begin();

    servoController.begin();
    ultrasonicSensor.begin();
    const bool imuReady = imuSensor.begin();
    Serial.println("AURA_ESP32_READY");
    if (!imuReady) {
        Serial.println("WARN:MPU6050_NOT_FOUND");
    }
}

void loop() {
    if (!Serial.available()) {
        return;
    }

    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command.length() == 0) {
        return;
    }

    Serial.println(commandDispatcher.handle(command));
}
