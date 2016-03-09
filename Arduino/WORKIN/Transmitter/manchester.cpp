#include "manchester.h"
#include "Arduino.h"
#include "CircularBuffer.h"
#include "TimerOne.h"

void manchester_init(){
	pinMode(CLOCK_IN, INPUT);
	pinMode(MANCHESTER_IN, INPUT);
	attachInterrupt(digitalPinToInterrupt(CLOCK_IN), CLOCK_ISR, CHANGE);
	Timer1.init(FREQUENCY*4, MANCHESTER_ISR);
}

CircularBuffer buffer(32);

void manchester_read(int *ptr){
	return buffer.read(ptr);
}


void MANCHESTER_ISR(){
	buffer.write(digitalRead(MANCHESTER_IN));
	Timer1.stop();
}

void CLOCK_ISR(){
		Timer1.start();
}

