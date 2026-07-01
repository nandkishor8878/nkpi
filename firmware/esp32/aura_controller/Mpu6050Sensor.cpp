#include "Mpu6050Sensor.h"

#include <Wire.h>

#include "config.h"

bool Mpu6050Sensor::begin() {
    Wire.beginTransmission(MPU6050_I2C_ADDRESS);
    Wire.write(MPU6050_PWR_MGMT_1);
    Wire.write(0);
    return Wire.endTransmission() == 0;
}

bool Mpu6050Sensor::isConnected() {
    Wire.beginTransmission(MPU6050_I2C_ADDRESS);
    return Wire.endTransmission() == 0;
}

bool Mpu6050Sensor::read(ImuReading& reading) {
    Wire.beginTransmission(MPU6050_I2C_ADDRESS);
    Wire.write(MPU6050_ACCEL_XOUT_H);

    if (Wire.endTransmission(false) != 0) {
        return false;
    }

    const uint8_t bytesRequested = 14;
    if (Wire.requestFrom(MPU6050_I2C_ADDRESS, bytesRequested) != bytesRequested) {
        return false;
    }

    const int16_t accelXRaw = readWord();
    const int16_t accelYRaw = readWord();
    const int16_t accelZRaw = readWord();
    readWord();
    const int16_t gyroXRaw = readWord();
    const int16_t gyroYRaw = readWord();
    const int16_t gyroZRaw = readWord();

    reading.accelX = accelXRaw / MPU6050_ACCEL_SCALE;
    reading.accelY = accelYRaw / MPU6050_ACCEL_SCALE;
    reading.accelZ = accelZRaw / MPU6050_ACCEL_SCALE;
    reading.gyroX = gyroXRaw / MPU6050_GYRO_SCALE;
    reading.gyroY = gyroYRaw / MPU6050_GYRO_SCALE;
    reading.gyroZ = gyroZRaw / MPU6050_GYRO_SCALE;
    return true;
}

String Mpu6050Sensor::status() {
    if (!isConnected()) {
        return "IMU_STATUS:CONNECTED:0:ADDRESS:0x68:ERROR:NOT_FOUND";
    }

    ImuReading reading;
    if (!read(reading)) {
        return "IMU_STATUS:CONNECTED:1:ADDRESS:0x68:ERROR:READ_FAILED";
    }

    return "IMU_STATUS:CONNECTED:1:ADDRESS:0x68:ERROR:NONE";
}

int16_t Mpu6050Sensor::readWord() {
    const uint8_t highByte = Wire.read();
    const uint8_t lowByte = Wire.read();
    return static_cast<int16_t>((highByte << 8) | lowByte);
}
