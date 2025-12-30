/**
 * @file BThomeV2_ESP32.cpp
 * @brief ESP32 implementation of BThome V2 using NimBLE
 */

#if defined(ESP32)

#include "BThomeV2.h"

// BThome V2 Service UUID: 0000fcd2-0000-1000-8000-00805f9b34fb
const uint16_t BTHOME_SERVICE_UUID_16 = 0xFCD2;

BThomeV2Device::BThomeV2Device() {}

BThomeV2Device::~BThomeV2Device() { end(); }

bool BThomeV2Device::begin(const char* devName) {
  if (initialized) {
    return true;
  }

  strncpy(deviceName, devName, sizeof(deviceName) - 1);
  deviceName[sizeof(deviceName) - 1] = '\0';

  // Initialize NimBLE
  NimBLEDevice::init(deviceName);

  // Get the advertising instance
  pAdvertising = NimBLEDevice::getAdvertising();
  if (!pAdvertising) {
    return false;
  }

  // Configure advertising
  // Note: setScanResponse, setMinPreferred, setMaxPreferred removed in
  // NimBLE 2.x
  pAdvertising->setMinInterval(0x06);  // 7.5ms min interval
  pAdvertising->setMaxInterval(0x12);  // 22.5ms max interval

  initialized = true;
  return true;
}

void BThomeV2Device::end() {
  if (!initialized) {
    return;
  }

  stopAdvertising();
  NimBLEDevice::deinit(true);
  initialized = false;
}

bool BThomeV2Device::startAdvertising() {
  if (!initialized) {
    return false;
  }

  // Build service data
  uint8_t serviceData[31];  // Max 31 bytes for BLE advertising
  size_t dataSize = buildServiceData(serviceData, sizeof(serviceData));

  if (dataSize == 0) {
    return false;
  }

  // Clear previous advertising data
  pAdvertising->reset();

  // Set advertising as non-connectable
  // Note: setAdvertisementType removed in NimBLE 2.x
  // Use setConnectableMode instead
  pAdvertising->setConnectableMode(BLE_GAP_CONN_MODE_NON);

  // Add service UUID
  NimBLEAdvertisementData advData;
  advData.setCompleteServices(NimBLEUUID(BTHOME_SERVICE_UUID_16));

  // Add device name
  advData.setName(deviceName);

  // Add service data
  std::string serviceDataStr((char*)serviceData, dataSize);
  advData.setServiceData(NimBLEUUID(BTHOME_SERVICE_UUID_16), serviceDataStr);

  // Set the advertising data
  pAdvertising->setAdvertisementData(advData);

  // Start advertising
  return pAdvertising->start();
}

void BThomeV2Device::stopAdvertising() {
  if (initialized && pAdvertising) {
    pAdvertising->stop();
  }
}

bool BThomeV2Device::setMAC(const uint8_t mac[6]) {
  if (!initialized) {
    // Need to set MAC before initialization
    // NimBLE doesn't easily support custom MAC after init
    return false;
  }

  // NimBLE uses the ESP32's hardware MAC by default
  // Custom MAC setting is complex with NimBLE and may require
  // setting it before NimBLEDevice::init()
  return false;
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

#endif  // ESP32
