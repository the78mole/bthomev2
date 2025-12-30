/**
 * @file BThomeV2_ESP32.h
 * @brief ESP32 implementation of BThome V2 using NimBLE
 */

#ifndef BTHOMEV2_ESP32_H
#define BTHOMEV2_ESP32_H

#if defined(ESP32)

#include "BThomeV2.h"
#include <NimBLEDevice.h>
#include <NimBLEAdvertising.h>

/**
 * @brief ESP32 implementation of BThome V2 using NimBLE stack
 */
class BThomeV2_ESP32 : public BThomeV2 {
public:
    BThomeV2_ESP32();
    virtual ~BThomeV2_ESP32();
    
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
    NimBLEAdvertising* pAdvertising = nullptr;
    char deviceName[32] = "BThome";
    bool initialized = false;
};

// Create a typedef for easier use
typedef BThomeV2_ESP32 BThomeV2Device;

#endif // ESP32

#endif // BTHOMEV2_ESP32_H
