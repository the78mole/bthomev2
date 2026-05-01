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

  // Check if SoftDevice S140 is present in flash BEFORE any SVC call.
  // The SoftDevice FWID sits at a fixed flash address (no SVC needed).
  // S140 v7.3.0 → FWID = 0x0123; 0xFFFF means no SoftDevice in flash.
  uint16_t sd_fwid = *(volatile uint16_t*)0x3004U;
  Serial.printf(
      "[DBG] SoftDevice FWID @ 0x3004: 0x%04X  (expect 0x0123 for S140 "
      "v7.3.0)\n",
      sd_fwid);
  Serial.flush();

  // Initialize Bluefruit - use default begin() without parameters
  Serial.println("[DBG] calling Bluefruit.begin()...");
  Serial.flush();
  Bluefruit.begin();
  Serial.println("[DBG] Bluefruit.begin() returned");

  // Set TX power to maximum for better range
  Bluefruit.setTxPower(4);  // Max power

  Bluefruit.setName(deviceName);

  // Set up advertising parameters
  Bluefruit.Advertising.restartOnDisconnect(true);
  Bluefruit.Advertising.setInterval(32, 244);  // in unit of 0.625 ms
  Bluefruit.Advertising.setFastTimeout(30);    // seconds

  // Put device name in scan response (saves space in advertising packet).
  // The advertising packet budget is 31 bytes:
  //   Flags(3) + TxPower(3) + ServiceData(~13) = ~19 bytes used.
  // A 17-char name would need 19 bytes and cause overflow if put in adv packet.
  Bluefruit.ScanResponse.addName();

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

  Serial.printf("[DBG] getAdvertisementData size=%u\n", (unsigned)size);
  if (size == 0) {
    Serial.println("[DBG] ERROR: size==0, aborting");
    return false;
  }

  // Print raw buffer
  Serial.print("[DBG] raw buffer: ");
  for (size_t i = 0; i < size; i++) {
    Serial.printf("%02X ", advertisementData[i]);
  }
  Serial.println();

  // Stop current advertising if running
  if (advertising) {
    Bluefruit.Advertising.stop();
  }

  // Clear advertising data
  Bluefruit.Advertising.clearData();

  // Extract service data payload from the advertisement buffer.
  // Buffer layout from getAdvertisementData():
  //   [0]=FLAG1(0x02) [1]=FLAG2(0x01) [2]=FLAG3(0x06)
  //   [3]=sd_length   [4]=0x16        [5]=UUID1(0xD2) [6]=UUID2(0xFC)
  //   [7]=indicator   [8..]=measurement bytes
  // addData(0x16, data, len) builds: [len+1][0x16][data...]
  // So pass data = &advertisementData[5] (UUID+indicator+measurements),
  // len = sd_length - 1 (sd_length counts the 0x16 type byte too).
  uint8_t sd_length = advertisementData[3];
  Serial.printf("[DBG] sd_length=%u, payload len=%u\n", sd_length,
                sd_length - 1);
  Serial.print("[DBG] svc payload: ");
  for (uint8_t i = 0; i < sd_length - 1; i++) {
    Serial.printf("%02X ", advertisementData[5 + i]);
  }
  Serial.println();

  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();
  Bluefruit.Advertising.addData(0x16, &advertisementData[5], sd_length - 1);

  // Start advertising (0 = Don't stop advertising)
  bool started = Bluefruit.Advertising.start(0);
  Serial.printf("[DBG] Advertising.start(0) = %s\n", started ? "OK" : "FAILED");
  if (started) {
    advertising = true;
    return true;
  }

  return false;
}

#endif  // NRF52
