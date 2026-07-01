#pragma once

#include <Arduino.h>

#include "Mpu6050Sensor.h"
#include "ServoController.h"
#include "UltrasonicSensor.h"

class CommandDispatcher {
public:
    CommandDispatcher(
        ServoController& servoController,
        UltrasonicSensor& ultrasonicSensor,
        Mpu6050Sensor& imuSensor
    );

    String handle(const String& command);

private:
    ServoController& servoController;
    UltrasonicSensor& ultrasonicSensor;
    Mpu6050Sensor& imuSensor;

    String handleServoCommand(const String& command);
    String handleDistanceCommand();
    String handleImuCommand();
    bool parseUnsignedByte(const String& value, uint8_t& result) const;
};
