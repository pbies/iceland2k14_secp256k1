#pragma once
#include <stdint.h>
#include <string>

class Keccak {
public:
	enum Bits { KECCAK224 = 224, KECCAK256 = 256, KECCAK384 = 384, KECCAK512 = 512 };

	explicit Keccak(Bits bits = KECCAK256);

	void reset();
	void add(const void *data, size_t numBytes);
	void processBuffer();
	void processBlock(const void *data);
	std::string getHash();
	void getHash(uint8_t *hash);

	std::string operator()(const void *data, size_t numBytes);
	void operator()(const void *data, size_t numBytes, uint8_t *hash);
	std::string operator()(const std::string &data);

private:
	uint64_t m_hash[25];
	size_t   m_blockSize;
	size_t   m_bits;
	uint8_t  m_buffer[144];
	size_t   m_bufferSize;
};
