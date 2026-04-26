#include <Arduino.h>

//
const int IN1=2;
const int IN2=3;
const int ENA=5;

const int IN3=4;
const int IN4=7;
const int ENB=6;
//

class Robot {
public:
	void begin() {
		Serial.begin(115200);

		//
		pinMode(IN1, OUTPUT);
		pinMode(IN2, OUTPUT);
		pinMode(ENA, OUTPUT);

		pinMode(IN3, OUTPUT);
		pinMode(IN4, OUTPUT);
		pinMode(ENB, OUTPUT);
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

	void processCommand(String inp) {
		char cmd_type = inp.charAt(0);

		if (cmd_type == 'M') {
			int speed = inp.substring(2).toInt();

			// motor control logic
			//
			digitalWrite(IN1, HIGH);
			digitalWrite(IN2, LOW);
			digitalWrite(IN3, HIGH);
			digitalWrite(IN4, LOW);

			analogWrite(ENA, speed);
			analogWrite(ENB, speed);
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
				digitalWrite(IN1, HIGH);
				digitalWrite(IN2, LOW);
				digitalWrite(IN3, LOW);
				digitalWrite(IN4, HIGH);

				analogWrite(ENA, speed);
				analogWrite(ENB, speed);
			} 
			else if (direction == 0) {
				digitalWrite(IN1, LOW);
				digitalWrite(IN2, HIGH);
				digitalWrite(IN3, HIGH);
				digitalWrite(IN4, LOW);

				analogWrite(ENA, speed);
				analogWrite(ENB, speed);
			}

			delay(duration);

			digitalWrite(ENA, LOW);
			digitalWrite(ENB, LOW);
			//

			Serial.println("OK");
		} else if (cmd_type == 'X') {
			
			// motor stop logic
			//
			digitalWrite(IN1, LOW);
			digitalWrite(IN2, LOW);
			digitalWrite(IN3, LOW);
			digitalWrite(IN4, LOW);
			digitalWrite(ENA, LOW);
			digitalWrite(ENB, LOW);
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