#pragma once

#include <Arduino.h>

#include "ServoController.h"

class CommandDispatcher {
public:
    explicit CommandDispatcher(ServoController& servoController);

    String handle(const String& command);

private:
    ServoController& servoController;

    String handleServoCommand(const String& command);
    bool parseUnsignedByte(const String& value, uint8_t& result) const;
};

