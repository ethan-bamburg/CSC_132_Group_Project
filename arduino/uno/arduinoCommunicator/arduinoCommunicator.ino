
bool paired = false;

void setup() {
  // make sure it's the same as python communicator
  Serial.begin(9600);
}

void loop() {
  // are we connected to serial?
  if (Serial.available()) {
    // read the line, store it
    String line = Serial.readStringUntil('\n');

    // if we aren't paired and we're asked to, let's do it
    if(!paired && line == "PAIR") {
      Serial.println("PAIR_OK");
    }
    else {
      if(line == "GET_DATA") {
        Serial.println("DATA");
      }
      else if(line.startsWith("SET: ")) {
        Serial.println("ACK");
      }
    }
  }
    
}