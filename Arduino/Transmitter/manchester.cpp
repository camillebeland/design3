#include "manchester.h"
#include "Arduino.h"
#include "CircularBuffer.h"
#include "TimerOne.h"

void manchester_init(){
	pinMode(CLOCK_IN, INPUT);
	pinMode(MANCHESTER_IN, INPUT);
	attachInterrupt(digitalPinToInterrupt(CLOCK_IN), CLOCK_ISR, CHANGE);
	Timer1.init(FREQUENCY, MANCHESTER_ISR);
}

CircularBuffer buffer(32);
int clock_count = 0;
int last_clock_count = clock_count;

void manchester_get(){
	if (last_clock_count != clock_count){
		last_clock_count = clock_count;
		buffer.write(digitalRead(MANCHESTER_IN));
		Timer1.stop();
	}
}

void manchester_read(int *ptr){
	return buffer.read(ptr);
}


void MANCHESTER_ISR(){
	clock_count++;
}

void CLOCK_ISR(){
		Timer1.start();
}

