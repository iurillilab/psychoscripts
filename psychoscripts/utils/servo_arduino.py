"""Control the movement of a servo motor using Arduino.
Arduino firmware required:

#include <Servo.h>
Servo myservo;

int finalLocation;
int delayPerDegreeMSec;
int delayBeforeGoingHomeSec;

int servoMovingToward = 12;
int servoMovingHome = 11;

int homePosition = 10;

void setup() {
  pinMode(servoMovingHome, OUTPUT);
  pinMode(servoMovingToward, OUTPUT);

  myservo.attach(6); //attaches the servo to pin 6
  myservo.write(homePosition);
  delay(1000); //not sure this is needed
  digitalWrite(servoMovingToward, LOW);
  digitalWrite(servoMovingHome, LOW);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    int finalLocation = Serial.parseInt(); Serial.read();
    int delayPerDegreeMSec = Serial.parseInt(); Serial.read();
    int delayBeforeGoingHomeSec = Serial.parseInt(); Serial.read();

    // Move to final point:
    int currentpos = myservo.read();
    digitalWrite(servoMovingToward, HIGH);
    while (currentpos < finalLocation) {
      currentpos++;
      myservo.write(currentpos);
      delay(delayPerDegreeMSec);
    }
    digitalWrite(servoMovingToward, LOW);

    // Pause:
    delay(delayBeforeGoingHomeSec);

    // Move back home:
    currentpos = myservo.read();
    digitalWrite(servoMovingHome, HIGH);
    while (currentpos > homePosition) {
      currentpos--;
      myservo.write(currentpos);
      delay(delayPerDegreeMSec);
    }
    digitalWrite(servoMovingHome, LOW);
  }
}

"""


def move_piezo(serial_port, final_position, step_interval_ms, pause_between_ms):
    """Move a servo moto using an arduino."""
    # create the message
    # mex = bytes([final_position, step_interval_ms, pause_between_ms])

    # write to serial port:
    # serial_port.write(mex)

    mex = f"{final_position};{step_interval_ms};{pause_between_ms}"

    # write to serial port:
    serial_port.write(bytes(mex, encoding="utf-8"))