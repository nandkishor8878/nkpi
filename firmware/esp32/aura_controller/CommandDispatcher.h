#pragma once

#include <Arduino.h>

#include "ServoController.h"
#include "UltrasonicSensor.h"

class CommandDispatcher {
public:
    CommandDispatcher(
        ServoController& servoController,
        UltrasonicSensor& ultrasonicSensor
    );

    String handle(const String& command);

private:
    ServoController& servoController;
    UltrasonicSensor& ultrasonicSensor;

    String handleServoCommand(const String& command);
    String handleDistanceCommand();
    bool parseUnsignedByte(const String& value, uint8_t& result) const;
};
