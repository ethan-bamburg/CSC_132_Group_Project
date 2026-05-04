#include <Servo.h>

// SERVO PINS
const int SERV_PIN = 2;

// MOTOR CONTROLLER PINS
const int MC_ENA_PIN = 10;
const int MC_IN1_PIN = 9;
const int MC_IN2_PIN = 8;

// SENSOR PINS


// IR PINS

// MOTOR SPEED 0 - 255

// VARIABLES
bool motorEnabled = true;
bool servoEnabled = true;

int motorSpeed = 100;
int servoDirection = 0;


Servo myServo;

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

void loop() {
  // put your main code here, to run repeatedly:

  // MOVE SERVO TO 0

  // SET MOTOR TO STOP
  digitalWrite(MC_IN1_PIN, LOW);
  digitalWrite(MC_IN2_PIN, LOW);
  analogWrite(MC_ENA_PIN, 0);

  myServo.write(0);

  delay(3000);
  // MOVE SERVO TO 180
  myServo.write(180);

  delay(3000);

  // SET MOTOR TO RUN CLOCKWISE AT 100 SPEED
  digitalWrite(MC_IN1_PIN, HIGH);
  digitalWrite(MC_IN2_PIN, LOW);
  analogWrite(MC_ENA_PIN, 100);

  delay(2000);

}
