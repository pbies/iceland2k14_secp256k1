#pragma once
#include <stdint.h>
#include <string>

class Timer {
public:
	static void Init();
	static uint64_t get_tick();
	static void SleepMillis(uint32_t millis);
	static int getCoreNumber();
	static uint32_t getSeed32();
	static std::string getSeed(int size);
	static void printResult(const char *unit, int unitSize, double t0, double t1);
	static std::string getResult(const char *unit, int unitSize, double t0, double t1);
};
