#include <Servo.h>
//#include <RH_ASK.h>
//#include <SPI.h>

// SERVO PINS
const int SERV_PIN = 2;

Servo myServo;

// MOTOR CONTROLLER PINS
const int MC_ENA_PIN = 10;
const int MC_IN1_PIN = 9;
const int MC_IN2_PIN = 8;

// SENSOR PINS

const int TEMP_PIN = A0;

// RF PINS

// speed, RX pin, TX pin
//RH_ASK driver(2000, 0, 1);

// MOTOR SPEED 0 - 255

// INTERNAL VARS

// 0- smart, 1- power, 2- comfort, 3- custom/basic
int fan_mode = 0;
int max_speed = 255;
int min_speed = 0;
int input_manage = 0;
float desired_temp = 20.0;

bool motorEnabled = true;
bool servoEnabled = true;
bool paired = false;

int motorSpeed = 100;
int servoDirection = 0;

float sensorVal = 20.0;
int oscilationStep = 0;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  // SET SERVO PIN
  myServo.attach(SERV_PIN);
  // SET MOTOR CONTROLLER PINS
  pinMode(MC_ENA_PIN, OUTPUT);
  pinMode(MC_IN1_PIN, OUTPUT);
  pinMode(MC_IN2_PIN, OUTPUT);

  Serial.println("Pins set...");
  
}

void serialWrapper(String msg) {
  Serial.println(msg);
}

void stopMotor() {
  // SET MOTOR TO STOP
  digitalWrite(MC_IN1_PIN, LOW);
  digitalWrite(MC_IN2_PIN, LOW);
  analogWrite(MC_ENA_PIN, 0);
}

void setMotorSpeed(int speed) {
  // CLOCKWISE
  digitalWrite(MC_IN1_PIN, HIGH);
  digitalWrite(MC_IN2_PIN, LOW);
  analogWrite(MC_ENA_PIN, speed);
}

void performOscilation() {
  // CHECK IF OSCILIATION ENABLED
  if(oscilationStep >= 3) {
    oscilationStep = 0;
  }
  else {
    oscilationStep += 1;
    return;
  }

  if (servoEnabled) {
    if (servoDirection >= 180) {
      myServo.write(0);
      servoDirection = 0;
    }
    else {
      myServo.write(180);
      servoDirection = 180;
    }
  }
  else {
    // SET FAN STRAIGHT
    myServo.write(90);
    servoDirection = 90;
  }
}

void serialSendInfo() {
  Serial.println("T:" + String(sensorVal) );
}

void loop() {
  // put your main code here, to run repeatedly:

  // TEMP READING
  sensorVal = analogRead(TEMP_PIN);

  // SERIAL COMMUNICATOR

  if (Serial.available()) {
    // read the line, store it
    String line = Serial.readStringUntil('\n');

    // if we aren't paired and we're asked to, let's do it
    if(!paired && line == "PAIR") {
      Serial.println("PAIR_OK");
      paired = true;
    }
    else if(paired) {
      if(line == "GET_DATA") {
        Serial.println(sensorVal/10);
      }
      else if(line.startsWith("SET: ")) {
        // MODE CHANGE
        if(line.substring(5).startsWith("MC")) {
          fan_mode = line.substring(7).toInt();
        }
        // DESIRED TEMP CHANGE
        else if(line.substring(5).startsWith("DTC")) {
          desired_temp = line.substring(8).toInt();
        }
        // MIN FAN
        else if(line.substring(5).startsWith("MIF")) {
          min_speed = line.substring(8).toInt();
        }
        // MAX FAN
        else if(line.substring(5).startsWith("MAF")) {
          max_speed = line.substring(8).toInt();
        }
        // TOGGLE OSCILATION
        else if(line.substring(5).startsWith("T_O")) {
          servoEnabled = !servoEnabled;
        }
        // INPUT CHANGE
        else if(line.substring(5).startsWith("IC")) {
          input_manage = line.substring(7).toInt();
        }
      }
    }
  }

  // performOscilation();

  if(fan_mode == 0) {
    float rpm = sensorVal/9;
    setMotorSpeed(constrain(rpm, min_speed, max_speed));

  }
  else if(fan_mode == 1) {
    float rpm = sensorVal/10;
    setMotorSpeed(constrain(rpm, min_speed, max_speed));
  }

  delay(500);


}
