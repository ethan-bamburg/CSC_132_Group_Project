#define MAX_RETRIES 5 // times before resetting connection

int retryCount = 0; // track times we've tried
bool paired = false; // machine
bool ready = false; // state

unsigned long lastSendTime = 0; // track time
const int interval = 1000; // 1 second between pings

void setup() {
  // make sure it's the same as python communicator
  Serial.begin(9600);
}

void loop() {
  // are we connected to serial?
  if (Serial.available()) {
    // read the line, store it
    String response = Serial.readStringUntil('\n');

    // if we are acknowledged, start printing
    if (response.indexOf("{ACK}") != -1) {
      retryCount = 0;

      // we are paired
      if (!paired) {
        paired = true;
        Serial.println("{PAIR FOUND}");
      } 
      else if (!ready) {  // ready to send data
        ready = true;
        Serial.println("{READY}");
      }
    }
  }

  // time control (like chaos control)
  if (millis() - lastSendTime > interval) {
    lastSendTime = millis();

    // if we aren't paired, ask for a pair
    if (!paired) {
      sendWithRetry("{PAIR}");
    }
    // if we aren't ready, ask for readiness
    else if (!ready) {
      sendWithRetry("{READY}");
    }
    // just send the stuff out, INFO in this case will be data we send
    else {
      sendWithRetry("{INFO}");
    }
  }
}

void sendWithRetry(String message) {
  // keep printing this message
  // for however many times
  // we need to retry
  if (retryCount >= MAX_RETRIES) {
    // reset everything
    Serial.println("{RESETTING}");
    paired = false;
    ready = false;
    retryCount = 0;
    return;
  }

  Serial.println(message);
  retryCount++;
}