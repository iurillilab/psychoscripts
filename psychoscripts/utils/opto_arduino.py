"""Control the generation of periodic TTL pulses for optogenetic stimulation.
Arduino firmware required:

// Arduino_controlled_LASER_Stimulation

int pulsePin = 9;

void setup() {
  //start USB connection with the computer
  Serial.begin(9600);

}

void loop() {

  //wait for serial input
  if(Serial.available() > 0){

    //read three inputs from serial port and get rid of separator char
    //parseInt reads a string input until it finds a non-numerical character
    //from matlab/python, send input as a single string of the form eg "100;8;5000"
    int frequency = Serial.parseInt(); Serial.read();
    int pulseDurationMs = Serial.parseInt(); Serial.read();
    long int stimulusDurationMs = Serial.parseInt(); Serial.read();

    int durationOff = (1000 / frequency) - pulseDurationMs;
    long int elapsed_time = 0;

    int startTime = millis();
    if (stimulusDurationMs > 0) {
      while((millis() - startTime) <= stimulusDurationMs){
      // Laser ON
      digitalWrite(pulsePin, HIGH);
      delay(pulseDurationMs);

      digitalWrite(pulsePin, LOW);
      delay(durationOff);
      }
    }
  }
}
"""


def laser_pulses(serial_port, frequency, pulse_duration_ms, stim_len_s):
    """Move a servo moto using an arduino."""
    # create the message

    mex = f"{frequency};{pulse_duration_ms};{stim_len_s};"

    # write to serial port:
    serial_port.write(bytes(mex, encoding="utf-8"))
