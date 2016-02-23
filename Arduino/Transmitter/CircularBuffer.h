#ifndef CircularBuffer_h
#define CircularBuffer_h

class CircularBuffer{

public:
	CircularBuffer(int size);
	void write(int data);
	void read(int * ptr);
private:
	int *buffer;
	int readIndex;
	int writeIndex;
	int bufferSize;
};
#endif 
