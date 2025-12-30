/**
 * @file BThomeV2_nRF52.h
 * @brief nRF52 implementation of BThome V2 using Adafruit nRF52
 */

#ifndef BTHOMEV2_NRF52_H
#define BTHOMEV2_NRF52_H

#if defined(NRF52) || defined(NRF52840_XXAA) || defined(ARDUINO_NRF52_ADAFRUIT)

#include "BThomeV2.h"
#include <bluefruit.h>

/**
 * @brief nRF52 implementation of BThome V2 using Adafruit Bluefruit library
 */
class BThomeV2_nRF52 : public BThomeV2 {
public:
    BThomeV2_nRF52();
    virtual ~BThomeV2_nRF52();
    
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

// Create a typedef for easier use
typedef BThomeV2_nRF52 BThomeV2Device;

#endif // NRF52

#endif // BTHOMEV2_NRF52_H
