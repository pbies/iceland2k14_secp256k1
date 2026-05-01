#pragma once
#include <stdint.h>
#include <stdlib.h>

class CSHA256 {
public:
	static const size_t OUTPUT_SIZE = 32;

	CSHA256();
	CSHA256 &Write(const uint8_t *data, size_t len);
	void Finalize(uint8_t *hash);
	CSHA256 &Reset() { return *this = CSHA256(); }

private:
	uint32_t s[8];
	uint8_t  buf[64];
	uint64_t bytes;
};

class _sha256 {
public:
	static void Initialize(uint32_t *s);
	static void Transform(uint32_t *s, const uint8_t *chunk);
	static void Transform2(uint32_t *s, const uint8_t *chunk);
};
