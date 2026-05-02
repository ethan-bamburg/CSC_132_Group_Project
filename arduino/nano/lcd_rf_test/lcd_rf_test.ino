#include <RH_ASK.h>
#include <SPI.h>
#include <LiquidCrystal.h>

// RF: speed, RX pin, TX pin
RH_ASK driver(2000, 7, 6);

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

const char *msg = "test message";

unsigned long lastSend = 0;

void setup() {
  driver.init();
  lcd.begin(16, 2);
  lcd.print("RF Test");
}

void loop() {

  if (millis() - lastSend > 2000) {
    const char *msg = "Hello RF";

    driver.send((uint8_t *)msg, strlen(msg));
    driver.waitPacketSent();

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