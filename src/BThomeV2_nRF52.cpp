/**
 * @file BThomeV2_nRF52.cpp
 * @brief nRF52 implementation of BThome V2 using Adafruit Bluefruit
 */

#if defined(NRF52) || defined(NRF52840_XXAA) || defined(ARDUINO_NRF52_ADAFRUIT)

#include "BThomeV2.h"

// BThome V2 Service UUID: 0000fcd2-0000-1000-8000-00805f9b34fb
const uint16_t BTHOME_SVC_UUID = 0xFCD2;

BThomeV2Device::BThomeV2Device() {
}

BThomeV2Device::~BThomeV2Device() {
    end();
}

bool BThomeV2Device::begin(const char* devName) {
    if (initialized) {
        return true;
    }
    
    strncpy(deviceName, devName, sizeof(deviceName) - 1);
    deviceName[sizeof(deviceName) - 1] = '\0';
    
    // Initialize Bluefruit
    Bluefruit.begin();
    Bluefruit.setName(deviceName);
    
    // Set up advertising parameters
    Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
    Bluefruit.Advertising.addTxPower();
    
    // Set connection interval (not connectable in beacon mode)
    Bluefruit.Advertising.restartOnDisconnect(true);
    Bluefruit.Advertising.setInterval(32, 244); // in unit of 0.625 ms
    Bluefruit.Advertising.setFastTimeout(30);   // seconds
    
    initialized = true;
    return true;
}

void BThomeV2Device::end() {
    if (!initialized) {
        return;
    }
    
    stopAdvertising();
    initialized = false;
}

bool BThomeV2Device::startAdvertising() {
    if (!initialized) {
        return false;
    }
    
    // Build service data payload
    uint8_t payload[31]; // Max 31 bytes for BLE advertising
    size_t payloadSize = buildServiceData(payload, sizeof(payload));
    
    if (payloadSize == 0) {
        return false;
    }
    
    // Stop current advertising if running
    if (advertising) {
        Bluefruit.Advertising.stop();
    }
    
    // Clear advertising data
    Bluefruit.Advertising.clearData();
    
    // Add flags and TX power
    Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
    Bluefruit.Advertising.addTxPower();
    
    // Add service UUID
    Bluefruit.Advertising.addService(BTHOME_SVC_UUID);
    
    // Build service data with UUID prefix (little endian)
    uint8_t serviceData[33]; // UUID (2 bytes) + payload
    serviceData[0] = BTHOME_SVC_UUID & 0xFF;
    serviceData[1] = (BTHOME_SVC_UUID >> 8) & 0xFF;
    memcpy(&serviceData[2], payload, payloadSize);
    
    // Add service data (UUID + data)
    Bluefruit.Advertising.addData(BLE_GAP_AD_TYPE_SERVICE_DATA_16BIT_UUID, 
                                   serviceData, payloadSize + 2);
    
    // Start advertising (0 = Don't stop advertising)
    if (Bluefruit.Advertising.start(0)) {
        advertising = true;
        return true;
    }
    
    return false;
}

void BThomeV2Device::stopAdvertising() {
    if (initialized && advertising) {
        Bluefruit.Advertising.stop();
        advertising = false;
    }
}

bool BThomeV2Device::setMAC(const uint8_t mac[6]) {
    if (!initialized) {
        return false;
    }
    
    // Adafruit nRF52 supports setting custom MAC address
    // Note: This should be called before begin() for best results
    // Format: MAC address as 6 bytes in reverse order (LSB first)
    uint8_t reversedMAC[6];
    for (int i = 0; i < 6; i++) {
        reversedMAC[i] = mac[5 - i];
    }
    
    // Set the MAC address
    // Note: Bluefruit.setAddr() expects address in LSB order
    return (Bluefruit.setAddr(reversedMAC) == 0);
}

bool BThomeV2Device::updateAdvertising() {
    if (!initialized) {
        return false;
    }
    
    // Stop current advertising
    stopAdvertising();
    
    // Start with new data
    return startAdvertising();
}

#endif // NRF52
