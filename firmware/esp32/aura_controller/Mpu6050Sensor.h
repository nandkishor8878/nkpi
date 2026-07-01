#pragma once

#include <Arduino.h>

struct ImuReading {
    float accelX;
    float accelY;
    float accelZ;
    float gyroX;
    float gyroY;
    float gyroZ;
};

class Mpu6050Sensor {
public:
    bool begin();
    bool read(ImuReading& reading);

private:
    int16_t readWord();
};

