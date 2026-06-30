#include <Arduino.h>
#include <Wire.h>

#include "CommandDispatcher.h"
#include "ServoController.h"
#include "UltrasonicSensor.h"
#include "config.h"

ServoController servoController;
UltrasonicSensor ultrasonicSensor;
CommandDispatcher commandDispatcher(servoController, ultrasonicSensor);

void setup() {
    pinMode(STATUS_LED_PIN, OUTPUT);
    digitalWrite(STATUS_LED_PIN, LOW);

    Serial.begin(SERIAL_BAUD_RATE);
    Wire.begin();

    servoController.begin();
    ultrasonicSensor.begin();
    Serial.println("AURA_ESP32_READY");
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
