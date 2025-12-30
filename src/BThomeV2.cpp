/**
 * @file BThomeV2.cpp
 * @brief BThome V2 base implementation
 */

#include "BThomeV2.h"

// BThome V2 Service UUID: 0000181c-0000-1000-8000-00805f9b34fb
const uint16_t BTHOME_SERVICE_UUID = 0x181C;

void BThomeV2::clearMeasurements() {
    measurements.clear();
}

void BThomeV2::addTemperature(float temperature) {
    // Temperature in 0.01 °C, signed 16-bit
    int16_t temp = (int16_t)(temperature * 100.0f);
    std::vector<uint8_t> data;
    encodeInt16(temp, data);
    measurements.push_back(BThomeMeasurement(TEMPERATURE, data));
}

void BThomeV2::addHumidity(float humidity) {
    // Humidity in 0.01 %, unsigned 16-bit
    uint16_t hum = (uint16_t)(humidity * 100.0f);
    std::vector<uint8_t> data;
    encodeUInt16(hum, data);
    measurements.push_back(BThomeMeasurement(HUMIDITY, data));
}

void BThomeV2::addBattery(uint8_t battery) {
    // Battery in %, unsigned 8-bit
    std::vector<uint8_t> data;
    data.push_back(battery);
    measurements.push_back(BThomeMeasurement(BATTERY, data));
}

void BThomeV2::addPressure(float pressure) {
    // Pressure in 0.01 hPa, unsigned 24-bit
    uint32_t press = (uint32_t)(pressure * 100.0f);
    std::vector<uint8_t> data;
    encodeUInt24(press, data);
    measurements.push_back(BThomeMeasurement(PRESSURE, data));
}

void BThomeV2::addIlluminance(float illuminance) {
    // Illuminance in 0.01 lux, unsigned 24-bit
    uint32_t illum = (uint32_t)(illuminance * 100.0f);
    std::vector<uint8_t> data;
    encodeUInt24(illum, data);
    measurements.push_back(BThomeMeasurement(ILLUMINANCE, data));
}

void BThomeV2::addCO2(uint16_t co2) {
    // CO2 in ppm, unsigned 16-bit
    std::vector<uint8_t> data;
    encodeUInt16(co2, data);
    measurements.push_back(BThomeMeasurement(CO2, data));
}

void BThomeV2::addBinarySensor(BThomeObjectID objectId, bool state) {
    // Binary sensor, 1 byte (0 or 1)
    std::vector<uint8_t> data;
    data.push_back(state ? 0x01 : 0x00);
    measurements.push_back(BThomeMeasurement(objectId, data));
}

void BThomeV2::addButtonEvent(uint8_t event) {
    // Button event, 1 byte
    std::vector<uint8_t> data;
    data.push_back(event);
    measurements.push_back(BThomeMeasurement(BUTTON, data));
}

void BThomeV2::addMeasurement(BThomeObjectID objectId, const std::vector<uint8_t>& data) {
    measurements.push_back(BThomeMeasurement(objectId, data));
}

bool BThomeV2::setEncryptionKey(const uint8_t key[16]) {
    memcpy(encryptionKey, key, 16);
    return true;
}

void BThomeV2::setEncryption(bool enabled) {
    encryptionEnabled = enabled;
}

size_t BThomeV2::buildServiceData(uint8_t* output, size_t maxSize) {
    if (maxSize < 1) return 0;
    
    size_t pos = 0;
    
    // Device Information byte (bit 0: encryption, bit 1-4: reserved, bit 5-7: BTHome version)
    uint8_t deviceInfo = 0x40; // Version 2 (010 in bits 5-7)
    if (encryptionEnabled) {
        deviceInfo |= 0x01;
    }
    output[pos++] = deviceInfo;
    
    // If encrypted, add packet counter (not implemented in this basic version)
    if (encryptionEnabled) {
        if (pos + 4 > maxSize) return 0;
        output[pos++] = (packetCounter >> 0) & 0xFF;
        output[pos++] = (packetCounter >> 8) & 0xFF;
        output[pos++] = (packetCounter >> 16) & 0xFF;
        output[pos++] = (packetCounter >> 24) & 0xFF;
        packetCounter++;
    }
    
    // Add measurements
    for (const auto& measurement : measurements) {
        if (pos + 1 + measurement.data.size() > maxSize) {
            break; // Not enough space
        }
        
        output[pos++] = (uint8_t)measurement.objectId;
        
        for (uint8_t byte : measurement.data) {
            output[pos++] = byte;
        }
    }
    
    return pos;
}

void BThomeV2::encodeInt16(int16_t value, std::vector<uint8_t>& data) {
    data.push_back(value & 0xFF);
    data.push_back((value >> 8) & 0xFF);
}

void BThomeV2::encodeUInt16(uint16_t value, std::vector<uint8_t>& data) {
    data.push_back(value & 0xFF);
    data.push_back((value >> 8) & 0xFF);
}

void BThomeV2::encodeUInt24(uint32_t value, std::vector<uint8_t>& data) {
    data.push_back(value & 0xFF);
    data.push_back((value >> 8) & 0xFF);
    data.push_back((value >> 16) & 0xFF);
}
