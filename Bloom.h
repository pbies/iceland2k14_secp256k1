#pragma once
#include <stdint.h>
#include <stdlib.h>

class Bloom {
public:
	Bloom(uint64_t entries, double error);
	~Bloom();

	void add(const void *key, int len);
	bool check(const void *key, int len);
	int bloom_check_add(const void *key, int len, int add);
	bool test_bit_set_bit(uint8_t *buf, uint32_t x, int set);
	uint32_t murmurhash2(const void *key, int len, uint32_t seed);
	void print();
	void reset();
	void save(const char *filename);
	void load(const char *filename);

	uint8_t *get_bf();
	uint64_t get_bits();
	uint64_t get_bytes();
	uint32_t get_hashes();

private:
	uint64_t  bits;
	uint64_t  bytes;
	uint64_t  entries;
	uint32_t  hashes;
	double    bpe;
	uint8_t  *bf;
	bool      ready;
};
