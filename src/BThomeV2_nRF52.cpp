/**
 * @file BThomeV2_nRF52.cpp
 * @brief nRF52 implementation of BThome V2 using Adafruit Bluefruit
 *
 * This file implements the nRF52-specific BLE advertising using the
 * Adafruit Bluefruit library and the integrated BTHomeV2-Arduino encoding.
 */

#if defined(NRF52) || defined(NRF52840_XXAA) || defined(ARDUINO_NRF52_ADAFRUIT)

#include <bluefruit.h>

#include "BThomeV2.h"
#include "BtHomeV2Device.h"

// BThome V2 Service UUID: 0xFCD2
const uint16_t BTHOME_SVC_UUID = 0xFCD2;

BThomeV2Device::BThomeV2Device() : btHomeDevice(nullptr) {}

BThomeV2Device::~BThomeV2Device() { end(); }

bool BThomeV2Device::begin(const char* devName) {
  if (initialized) {
    return true;
  }

  strncpy(deviceName, devName, sizeof(deviceName) - 1);
  deviceName[sizeof(deviceName) - 1] = '\0';

  // Create BTHomeV2-Arduino device instance
  btHomeDevice = new ::BtHomeV2Device(devName, devName, false);
  if (!btHomeDevice) {
    return false;
  }

  // Initialize Bluefruit - use default begin() without parameters
  Bluefruit.begin();

  // Set TX power to maximum for better range
  Bluefruit.setTxPower(4);  // Max power

  Bluefruit.setName(deviceName);

  // Set up advertising parameters
  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();
  Bluefruit.Advertising.restartOnDisconnect(true);
  Bluefruit.Advertising.setInterval(32, 244);  // in unit of 0.625 ms
  Bluefruit.Advertising.setFastTimeout(30);    // seconds

  initialized = true;
  return true;
}

void BThomeV2Device::end() {
  if (!initialized) {
    return;
  }

  stopAdvertising();

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
  // Format: MAC address as 6 bytes in reverse order (LSB first)
  uint8_t reversedMAC[6];
  for (int i = 0; i < 6; i++) {
    reversedMAC[i] = mac[5 - i];
  }

  ble_gap_addr_t gap_addr;
  gap_addr.addr_type = BLE_GAP_ADDR_TYPE_RANDOM_STATIC;
  memcpy(gap_addr.addr, reversedMAC, 6);

  return Bluefruit.setAddr(&gap_addr);
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
          // Decode uint16 CO2 (ppm)
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

  if (size == 0) {
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

  // Add service data (BTHomeV2-Arduino already includes the UUID in the data)
  // Note: BLE_GAP_AD_TYPE_16BIT_SERVICE_UUID_COMPLETE = 0x03
  Bluefruit.Advertising.addData(0x16, advertisementData, size);

  // Start advertising (0 = Don't stop advertising)
  if (Bluefruit.Advertising.start(0)) {
    advertising = true;
    return true;
  }

  return false;
}

#endif  // NRF52
