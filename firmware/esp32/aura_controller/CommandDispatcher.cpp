#include "CommandDispatcher.h"

#include "config.h"

CommandDispatcher::CommandDispatcher(
    ServoController& servoController,
    UltrasonicSensor& ultrasonicSensor
) : servoController(servoController),
    ultrasonicSensor(ultrasonicSensor) {}

String CommandDispatcher::handle(const String& command) {
    if (command == "PING") {
        return "PONG";
    }

    if (command == "LED_ON") {
        digitalWrite(STATUS_LED_PIN, HIGH);
        return "OK";
    }

    if (command == "LED_OFF") {
        digitalWrite(STATUS_LED_PIN, LOW);
        return "OK";
    }

    if (command.startsWith("SERVO:")) {
        return handleServoCommand(command);
    }

    if (command == "READ:DISTANCE") {
        return handleDistanceCommand();
    }

    return "ERROR:UNKNOWN_COMMAND";
}

String CommandDispatcher::handleServoCommand(const String& command) {
    const int firstSeparator = command.indexOf(':');
    const int secondSeparator = command.indexOf(':', firstSeparator + 1);

    if (firstSeparator < 0 || secondSeparator < 0) {
        return "ERROR:INVALID_SERVO_COMMAND";
    }

    const String channelText = command.substring(firstSeparator + 1, secondSeparator);
    const String angleText = command.substring(secondSeparator + 1);

    uint8_t channel = 0;
    uint8_t angle = 0;

    if (!parseUnsignedByte(channelText, channel)) {
        return "ERROR:INVALID_SERVO_CHANNEL";
    }

    if (!parseUnsignedByte(angleText, angle)) {
        return "ERROR:INVALID_SERVO_ANGLE";
    }

    if (!servoController.setAngle(channel, angle)) {
        return "ERROR:SERVO_OUT_OF_RANGE";
    }

    return "OK";
}

String CommandDispatcher::handleDistanceCommand() {
    float distanceCm = 0.0;

    if (!ultrasonicSensor.readDistanceCm(distanceCm)) {
        return "ERROR:DISTANCE_TIMEOUT";
    }

    return "DISTANCE_CM:" + String(distanceCm, 1);
}

bool CommandDispatcher::parseUnsignedByte(const String& value, uint8_t& result) const {
    if (value.length() == 0) {
        return false;
    }

    for (size_t index = 0; index < value.length(); index++) {
        if (!isDigit(value[index])) {
            return false;
        }
    }

    const int parsedValue = value.toInt();
    if (parsedValue < 0 || parsedValue > 255) {
        return false;
    }

    result = static_cast<uint8_t>(parsedValue);
    return true;
}
