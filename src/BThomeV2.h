/**
 * @file BThomeV2.h
 * @brief BThome V2 protocol implementation for ESP32 and nRF52 platforms
 *
 * This library provides a unified interface for BLE advertising using the
 * BThome V2 format on ESP32 (via NimBLE) and nRF52 (via Adafruit nRF52)
 * platforms.
 */

#ifndef BTHOMEV2_H
#define BTHOMEV2_H

#include <Arduino.h>

#include <vector>

/**
 * @brief BThome V2 object IDs for sensor data
 *
 * Based on BThome V2 specification
 */
enum BThomeObjectID : uint8_t {
  // Sensor data
  PACKET_ID = 0x00,
  BATTERY = 0x01,
  TEMPERATURE = 0x02,
  HUMIDITY = 0x03,
  PRESSURE = 0x04,
  ILLUMINANCE = 0x05,
  MASS_KG = 0x06,
  MASS_LB = 0x07,
  DEW_POINT = 0x08,
  COUNT = 0x09,
  ENERGY = 0x0A,
  POWER = 0x0B,
  VOLTAGE = 0x0C,
  PM2_5 = 0x0D,
  PM10 = 0x0E,
  CO2 = 0x12,
  TVOC = 0x13,
  MOISTURE = 0x14,
  // Binary sensors
  BATTERY_LOW = 0x15,
  BATTERY_CHARGING = 0x16,
  CO = 0x17,
  COLD = 0x18,
  CONNECTIVITY = 0x19,
  DOOR = 0x1A,
  GARAGE_DOOR = 0x1B,
  GAS = 0x1C,
  HEAT = 0x1D,
  LIGHT = 0x1E,
  LOCK = 0x1F,
  MOISTURE_BINARY = 0x20,
  MOTION = 0x21,
  MOVING = 0x22,
  OCCUPANCY = 0x23,
  OPENING = 0x24,
  PLUG = 0x25,
  POWER_BINARY = 0x26,
  PRESENCE = 0x27,
  PROBLEM = 0x28,
  RUNNING = 0x29,
  SAFETY = 0x2A,
  SMOKE = 0x2B,
  SOUND = 0x2C,
  TAMPER = 0x2D,
  VIBRATION = 0x2E,
  WINDOW = 0x2F,
  // Events
  BUTTON = 0x3A,
  DIMMER = 0x3C
};

/**
 * @brief Structure to hold a single BThome measurement
 */
struct BThomeMeasurement {
  BThomeObjectID objectId;
  std::vector<uint8_t> data;

  BThomeMeasurement(BThomeObjectID id, const std::vector<uint8_t>& d)
      : objectId(id), data(d) {}
};

/**
 * @brief Abstract base class for BThome V2 implementation
 *
 * Platform-specific implementations (ESP32, nRF52) should inherit from this
 * class
 */
class BThomeV2 {
 public:
  virtual ~BThomeV2() {}

  /**
   * @brief Initialize the BLE stack
   * @param deviceName Name of the BLE device
   * @return true if initialization successful, false otherwise
   */
  virtual bool begin(const char* deviceName) = 0;

  /**
   * @brief Stop BLE advertising and deinitialize
   */
  virtual void end() = 0;

  /**
   * @brief Start BLE advertising
   * @return true if advertising started successfully, false otherwise
   */
  virtual bool startAdvertising() = 0;

  /**
   * @brief Stop BLE advertising
   */
  virtual void stopAdvertising() = 0;

  /**
   * @brief Set the MAC address for the device (if supported)
   * @param mac MAC address as 6 bytes
   * @return true if MAC was set successfully, false otherwise
   */
  virtual bool setMAC(const uint8_t mac[6]) = 0;

  /**
   * @brief Clear all measurements
   */
  void clearMeasurements();

  /**
   * @brief Add a temperature measurement (0.01 °C)
   * @param temperature Temperature in Celsius
   */
  void addTemperature(float temperature);

  /**
   * @brief Add a humidity measurement (0.01 %)
   * @param humidity Humidity in percent
   */
  void addHumidity(float humidity);

  /**
   * @brief Add a battery level measurement (%)
   * @param battery Battery level in percent (0-100)
   */
  void addBattery(uint8_t battery);

  /**
   * @brief Add a pressure measurement (0.01 hPa)
   * @param pressure Pressure in hPa
   */
  void addPressure(float pressure);

  /**
   * @brief Add an illuminance measurement (0.01 lux)
   * @param illuminance Illuminance in lux
   */
  void addIlluminance(float illuminance);

  /**
   * @brief Add a CO2 measurement (ppm)
   * @param co2 CO2 level in ppm
   */
  void addCO2(uint16_t co2);

  /**
   * @brief Add a binary sensor state
   * @param objectId Binary sensor object ID
   * @param state Sensor state (true/false)
   */
  void addBinarySensor(BThomeObjectID objectId, bool state);

  /**
   * @brief Add a button press event
   * @param event Event type (0x00=none, 0x01=press, 0x02=double_press,
   * 0x03=triple_press, 0x80=long_press)
   */
  void addButtonEvent(uint8_t event);

  /**
   * @brief Add a custom measurement
   * @param objectId Object ID from BThome specification
   * @param data Raw data bytes for the measurement
   */
  void addMeasurement(BThomeObjectID objectId,
                      const std::vector<uint8_t>& data);

  /**
   * @brief Set encryption key for encrypted advertising (if supported)
   * @param key 16-byte encryption key
   * @return true if encryption key was set, false otherwise
   */
  virtual bool setEncryptionKey(const uint8_t key[16]);

  /**
   * @brief Enable or disable encryption
   * @param enabled true to enable encryption, false to disable
   */
  void setEncryption(bool enabled);

  /**
   * @brief Check if encryption is enabled
   * @return true if encryption is enabled, false otherwise
   */
  bool isEncryptionEnabled() const { return encryptionEnabled; }

 protected:
  /**
   * @brief Build the service data payload for advertising
   * @param output Buffer to store the service data
   * @param maxSize Maximum size of the output buffer
   * @return Size of the service data, or 0 on error
   */
  size_t buildServiceData(uint8_t* output, size_t maxSize);

  std::vector<BThomeMeasurement> measurements;
  bool encryptionEnabled = false;
  uint8_t encryptionKey[16] = {0};
  uint32_t packetCounter = 0;

 private:
  void encodeInt16(int16_t value, std::vector<uint8_t>& data);
  void encodeUInt16(uint16_t value, std::vector<uint8_t>& data);
  void encodeUInt24(uint32_t value, std::vector<uint8_t>& data);
};

// Platform-specific device class
#if defined(ESP32)

#include <ArduinoBLE.h>

// Forward declaration for integrated BTHomeV2 encoding library
class BtHomeV2Device;

/**
 * @brief Platform-specific implementation of BThome V2
 *
 * This class provides the concrete implementation for ESP32 using ArduinoBLE
 * and the integrated BTHomeV2 encoding library.
 */
class BThomeV2Device : public BThomeV2 {
 public:
  BThomeV2Device();
  virtual ~BThomeV2Device();

  bool begin(const char* deviceName) override;
  void end() override;
  bool startAdvertising() override;
  void stopAdvertising() override;
  bool setMAC(const uint8_t mac[6]) override;

  /**
   * @brief Update advertising data with current measurements
   * Call this after adding/changing measurements to update the advertisement
   * @return true if advertising data was updated successfully
   */
  bool updateAdvertising();

 private:
  ::BtHomeV2Device*
      btHomeDevice;  // Pointer to integrated BTHomeV2 device instance
  char deviceName[32] = "BThome";
  bool initialized = false;
};

#elif defined(NRF52) || defined(NRF52840_XXAA) || \
    defined(ARDUINO_NRF52_ADAFRUIT)

#include <bluefruit.h>

/**
 * @brief Platform-specific implementation of BThome V2
 *
 * This class provides the concrete implementation for the current platform.
 * On ESP32, it uses NimBLE stack. On nRF52, it uses Adafruit Bluefruit.
 */
class BThomeV2Device : public BThomeV2 {
 public:
  BThomeV2Device();
  virtual ~BThomeV2Device();

  bool begin(const char* deviceName) override;
  void end() override;
  bool startAdvertising() override;
  void stopAdvertising() override;
  bool setMAC(const uint8_t mac[6]) override;

  /**
   * @brief Update advertising data with current measurements
   * Call this after adding/changing measurements to update the advertisement
   * @return true if advertising data was updated successfully
   */
  bool updateAdvertising();

 private:
  char deviceName[32] = "BThome";
  bool initialized = false;
  bool advertising = false;
};

#else
#error "Unsupported platform. This library supports ESP32 and nRF52 only."
#endif

#endif  // BTHOMEV2_H
