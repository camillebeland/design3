#ifndef TimerOne_h
#define TimerOne_h

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
