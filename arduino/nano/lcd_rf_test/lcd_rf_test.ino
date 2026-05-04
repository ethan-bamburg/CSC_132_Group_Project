// RF libs
#include <RH_ASK.h>
#include <SPI.h>
// LCD lib
#include <LiquidCrystal.h>

// RF: speed, RX pin, TX pin
RH_ASK driver(2000, 7, 6);
// LCD pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
// Button pins
const int ASK_DATA_PIN = A0;
const int TOG_OSCILATION_PIN = A1;
const int TOG_SMART_PIN = A2;
const int INC_TEMP_PIN = A3;
const int DEC_TEMP_PIN = A4;

// So we know who's communicating
const char *nanoID = "89Nano: ";

unsigned long lastSend = 0;

void setup() {
  driver.init();
  lcd.begin(16, 2);
  lcd.print("RF Test");
}

void loop() {

  if (millis() - lastSend > 2000) {

    sendRF();

    lastSend = millis();
  }

  uint8_t buf[20];
  uint8_t buflen = sizeof(buf);

  if (driver.recv(buf, &buflen)) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Received:");

    lcd.setCursor(0, 1);

    for (int i = 0; i < buflen; i++) {
      lcd.print((char)buf[i]);
    }
  }


}

void sendRF() {
  char message[50];
    snprintf(message, sizeof(message), "%s%s", nanoID, "Hello RF");

    driver.send((uint8_t *)message, strlen(message));
    driver.waitPacketSent();
}