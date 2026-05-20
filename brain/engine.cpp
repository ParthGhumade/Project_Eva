#include <Arduino.h>

//
// const int IN1=2;
// const int IN2=3;
// const int ENA=5;

// const int IN3=4;
// const int IN4=7;
// const int ENB=6;
//

//
#define L1 5
#define R1 6

#define L2 9
#define R2 10
//

class Robot {
public:
	void setup() {
		Serial.begin(115200);

		//
		pinMode(L1, OUTPUT);
		pinMode(R1, OUTPUT);

		pinMode(L2, OUTPUT);
		pinMode(R2, OUTPUT);
		//

		Serial.println("OK");
	}

	void loop() {
		if (Serial.available() > 0) {
			String input = Serial.readStringUntil('\n');
			input.trim();
			if (input.length() > 0) {
				processCommand(input);
			}
		}
	}

	void stop() {
		analogWrite(R1, 0);
		analogWrite(L1, 0);
		analogWrite(R2, 0);
		analogWrite(L2, 0);
		delay(1000);
	}

	void processCommand(String inp) {
		char cmd_type = inp.charAt(0);

		if (cmd_type == 'M') {
			int speed = inp.substring(2).toInt();

			// motor control logic
			//
			stop();
			analogWrite(R1, speed);
			analogWrite(L2, speed);
			//

			Serial.println("OK");
		} else if (cmd_type == 'T') {
			int direction = inp.charAt(2) - '0';
			int degrees = inp.substring(4).toInt();
			int speed = 100;
			int duration = degrees * 10; // need to calibrate this to perform a specific degree turn or we could consider the marker orientation in here

			// motor turn logic
			//
			if (direction == 1) {
				stop();
				analogWrite(R1, speed);
				analogWrite(R2, speed);
			} 
			else if (direction == 0) {
				stop();
				analogWrite(L1, speed);
				analogWrite(L2, speed);
			}

			delay(duration);

			stop();
			//

			Serial.println("OK");
		} else if (cmd_type == 'X') {
			
			// motor stop logic
			//
			stop();
			//

		} else if (cmd_type == 'C') {
			int level = inp.substring(2).toInt();

			// tof data reading logic VL53LOX
			// to be implemented later

			Serial.println(""); // update this to return real data
		} else {
			Serial.println("404");
		}
	}
};