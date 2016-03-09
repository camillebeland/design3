#ifndef TimerOne_h
#define TimerOne_h

#define RESOLUTION 65536
#define CPU_FREQUENCY 16000000
#define PRESCALER 8

class TimerOne{

public:
	void init(int freq, void (*isr)());
	void start();
	void stop();
	int counter;
	void (*isrCallback)();
};

extern TimerOne Timer1;

#endif 
