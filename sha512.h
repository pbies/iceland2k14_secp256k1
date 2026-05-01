#pragma once
#include <stdint.h>
#include <stdlib.h>

class CSHA512 {
public:
	static const size_t OUTPUT_SIZE = 64;

	CSHA512();
	void Initialize();
	CSHA512 &Write(const uint8_t *data, size_t len);
	void WriteDirect64(const uint8_t *data);
	void WriteDirect128(const uint8_t *data);
	void Finalize(uint8_t *hash);
	CSHA512 &Reset() { return *this = CSHA512(); }

private:
	uint64_t s[8];
	uint8_t  buf[128];
	uint64_t bytes[2];
};
