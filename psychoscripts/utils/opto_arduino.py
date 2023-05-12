"""Control the generation of periodic TTL pulses for optogenetic stimulation.
Arduino firmware required:

// Arduino_controlled_LASER_Stimulation

void setup() {
  //start USB connection with the computer
  Serial.begin(9600);
  delay(100);

}

void loop() {

    //wait for serial input
  if(Serial.available() > 0){
    //read three inputs from serial port and get rid of separator char
    //parseInt reads a string input until it finds a non-numerical character
    //from matlab, send input as a single string of the form "2000a8a"
      int frequency = Serial.parseInt(); Serial.read();
      int pulse_duration = Serial.parseInt(); Serial.read();
      int stimulus_duration = Serial.parseInt(); Serial.read();

      int starttime = millis();
      int endtime = starttime;
      int duration_off = (1000 / frequency) - pulse_duration;

      if (stimulus_duration > 0) {
        while((endtime - starttime) <= stimulus_duration){
        // Laser ON
        digitalWrite(13, HIGH);
        delay(pulse_duration);

        digitalWrite(13, LOW);
        delay(duration_off);

        endtime = millis();
      }
      }

      }
  }
"""


def move_piezo(serial_port, final_position, step_interval_ms, pause_between_s):
    """Move a servo moto using an arduino.
    """
    # create the message
    mex = bytes([final_position, step_interval_ms, pause_between_s])

    # write to serial port:
    serial_port.write(mex)
