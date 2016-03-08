#include "manchester.h"
#include "Arduino.h"
#include "CircularBuffer.h"
#include "TimerFour.h"

void manchester_init(){
	pinMode(CLOCK_IN, INPUT);
	pinMode(MANCHESTER_IN, INPUT);
	attachInterrupt(digitalPinToInterrupt(CLOCK_IN), CLOCK_ISR, CHANGE);
	Timer4.init(FREQUENCY*4, MANCHESTER_ISR);
}

CircularBuffer buffer(32);

void manchester_read(int *ptr){
	return buffer.read(ptr);
}


void MANCHESTER_ISR(){
	buffer.write(digitalRead(MANCHESTER_IN));
	Timer4.stop();
}

void CLOCK_ISR(){
		Timer4.start();
}

