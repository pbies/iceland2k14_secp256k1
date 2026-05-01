#pragma once
#include <stdint.h>
#include <stdlib.h>

class CRIPEMD160 {
public:
	static const size_t OUTPUT_SIZE = 20;

	CRIPEMD160();
	CRIPEMD160 &Write(const uint8_t *data, size_t len);
	void Finalize(uint8_t *hash);
	CRIPEMD160 &Reset() { return *this = CRIPEMD160(); }

private:
	uint32_t s[5];
	uint8_t  buf[64];
	uint64_t bytes;
};

class _ripemd160 {
public:
	static void Transform(uint32_t *s, const uint8_t *chunk);
};
