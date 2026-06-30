#pragma once

#include <Arduino.h>

class UltrasonicSensor {
public:
    void begin();
    bool readDistanceCm(float& distanceCm);
};

