#include "TimerOne.h"
#include <avr/io.h>
#include <avr/interrupt.h>

TimerOne Timer1;

ISR(TIMER1_OVF_vect)          // interrupt service routine that wraps a user defined function supplied by attachInterrupt
{
	TCNT1 = Timer1.counter;
	Timer1.isrCallback();
}


void TimerOne::init(int freq, void (*isr)()){
	
	isrCallback = isr;
	Timer1.counter = 65536-((16000000/8)/freq);
	TCCR1A = 0;
	TCCR1B = 0;
	//TCCR1B |=  (1 << CS41);  // 8 prescaler
	TIMSK1 |= (1 << TOIE1);   // enable timer overflow interrupt
	//TIMSK1 &= ~_BV(TOIE1);   // disable timer overflow interrupt
	//TCNT1 = counter;
}

void TimerOne::start(){
	TCNT1 = Timer1.counter;
	TCCR1B |=  (1 << CS11);  // 8 prescaler
}

void TimerOne::stop(){
	TCCR1B  = 0;
}
