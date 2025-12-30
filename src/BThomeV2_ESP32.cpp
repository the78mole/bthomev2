/**
 * @file BThomeV2_ESP32.cpp
 * @brief ESP32 implementation of BThome V2 using ArduinoBLE and
 * BTHomeV2-Arduino library
 */

#if defined(ESP32)

#include <ArduinoBLE.h>

#include "BThomeV2.h"
#include "BtHomeV2Device.h"

// BThome V2 Service UUID
const uint16_t BTHOME_SERVICE_UUID_16 = 0xFCD2;

BThomeV2Device::BThomeV2Device() : btHomeDevice(nullptr) {}

BThomeV2Device::~BThomeV2Device() {
  end();
  if (btHomeDevice) {
    delete btHomeDevice;
    btHomeDevice = nullptr;
  }
}

bool BThomeV2Device::begin(const char* devName) {
  if (initialized) {
    return true;
  }

  strncpy(deviceName, devName, sizeof(deviceName) - 1);
  deviceName[sizeof(deviceName) - 1] = '\0';

  // Initialize ArduinoBLE
  if (!BLE.begin()) {
    return false;
  }

  // Set device name and local name
  BLE.setDeviceName(deviceName);
  BLE.setLocalName(deviceName);

  // Create BTHomeV2-Arduino device instance
  if (btHomeDevice) {
    delete btHomeDevice;
  }
  btHomeDevice = new ::BtHomeV2Device(deviceName, deviceName, false);

  initialized = true;
  return true;
}

void BThomeV2Device::end() {
  if (!initialized) {
    return;
  }

  stopAdvertising();
  BLE.end();

  if (btHomeDevice) {
    delete btHomeDevice;
    btHomeDevice = nullptr;
  }

  initialized = false;
}

bool BThomeV2Device::startAdvertising() {
  if (!initialized || !btHomeDevice) {
    return false;
  }

  return updateAdvertising();
}

void BThomeV2Device::stopAdvertising() {
  if (initialized) {
    BLE.stopAdvertise();
  }
}

bool BThomeV2Device::setMAC(const uint8_t mac[6]) {
  // ArduinoBLE uses the ESP32's hardware MAC by default
  // Custom MAC setting requires platform-specific implementation
  return false;
}

bool BThomeV2Device::updateAdvertising() {
  if (!initialized || !btHomeDevice) {
    return false;
  }

  // Clear the BTHomeV2-Arduino device's measurement data
  btHomeDevice->clearMeasurementData();

  // Add all measurements from our base class to the BTHomeV2-Arduino device
  for (const auto& measurement : measurements) {
    switch (measurement.objectId) {
      case TEMPERATURE:
        if (measurement.data.size() == 2) {
          // Decode int16 temperature (0.01 °C resolution)
          int16_t temp =
              (int16_t)(measurement.data[0] | (measurement.data[1] << 8));
          btHomeDevice->addTemperature_neg327_to_327_Resolution_0_01(temp /
                                                                     100.0f);
        }
        break;

      case HUMIDITY:
        if (measurement.data.size() == 2) {
          // Decode uint16 humidity (0.01 % resolution)
          uint16_t hum =
              (uint16_t)(measurement.data[0] | (measurement.data[1] << 8));
          btHomeDevice->addHumidityPercent_Resolution_0_01(hum / 100.0f);
        }
        break;

      case BATTERY:
        if (measurement.data.size() == 1) {
          btHomeDevice->addBatteryPercentage(measurement.data[0]);
        }
        break;

      case PRESSURE:
        if (measurement.data.size() == 3) {
          // Decode uint24 pressure (0.01 hPa resolution)
          uint32_t pressure =
              (uint32_t)(measurement.data[0] | (measurement.data[1] << 8) |
                         (measurement.data[2] << 16));
          btHomeDevice->addPressureHpa(pressure / 100.0f);
        }
        break;

      case ILLUMINANCE:
        if (measurement.data.size() == 3) {
          // Decode uint24 illuminance (0.01 lux resolution)
          uint32_t lux =
              (uint32_t)(measurement.data[0] | (measurement.data[1] << 8) |
                         (measurement.data[2] << 16));
          btHomeDevice->addIlluminanceLux(lux / 100.0f);
        }
        break;

      case CO2:
        if (measurement.data.size() == 2) {
          uint16_t co2 =
              (uint16_t)(measurement.data[0] | (measurement.data[1] << 8));
          btHomeDevice->addCo2Ppm(co2);
        }
        break;

      // Binary sensors
      case BATTERY_LOW:
        if (measurement.data.size() == 1) {
          btHomeDevice->setBatteryState(
              measurement.data[0] ? BATTERY_STATE_LOW : BATTERY_STATE_NORMAL);
        }
        break;

      case MOTION:
        if (measurement.data.size() == 1) {
          btHomeDevice->setMotionState(measurement.data[0]
                                           ? Motion_Sensor_Status_Detected
                                           : Motion_Sensor_Status_Clear);
        }
        break;

      case DOOR:
        if (measurement.data.size() == 1) {
          btHomeDevice->setDoorState(measurement.data[0]
                                         ? Door_Sensor_Status_Open
                                         : Door_Sensor_Status_Closed);
        }
        break;

      case WINDOW:
        if (measurement.data.size() == 1) {
          btHomeDevice->setWindowState(measurement.data[0]
                                           ? Window_Sensor_Status_Open
                                           : Window_Sensor_Status_Closed);
        }
        break;

      case BUTTON:
        if (measurement.data.size() == 1) {
          btHomeDevice->setButtonEvent(
              (Button_Event_Status)measurement.data[0]);
        }
        break;

      default:
        // Unsupported sensor type - skip
        break;
    }
  }

  // Get the advertisement data from BTHomeV2-Arduino
  uint8_t advertisementData[MAX_ADVERTISEMENT_SIZE];
  size_t size = btHomeDevice->getAdvertisementData(advertisementData);

  if (size == 0 || size > MAX_ADVERTISEMENT_SIZE) {
    return false;
  }

  // Stop any existing advertising
  BLE.stopAdvertise();

  // Set raw advertising data
  BLEAdvertisingData advData;
  advData.setRawData(advertisementData, size);
  BLE.setAdvertisingData(advData);

  // Start advertising
  BLE.advertise();

  return true;
}

#endif  // ESP32
