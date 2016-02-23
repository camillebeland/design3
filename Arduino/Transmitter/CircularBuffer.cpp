#include "CircularBuffer.h"
#include <stdio.h>
#include <string.h>

CircularBuffer::CircularBuffer(int size){
	buffer = new int[size];
	memset(buffer, 0, size*sizeof(int*)); 
	readIndex = 0;
	writeIndex = 0;
	bufferSize = size;
}

void CircularBuffer::write(int data){
	buffer[writeIndex] = data;
	writeIndex = (writeIndex+1)%bufferSize;
}

void CircularBuffer::read(int* ptr){
	memcpy(ptr, buffer, bufferSize*sizeof(int));
}

