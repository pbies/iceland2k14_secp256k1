#pragma once
#include <stdint.h>
#include <emmintrin.h>  /* SSE2 */

/* _sha256sse: SSE4.1 implementation processing 2 blocks in parallel.
 * State vector: __m128i[8] holding two SHA256 states interleaved. */
class _sha256sse {
public:
	static void Initialize(__m128i *s);
	static void Transform(__m128i *s, uint32_t *m0, uint32_t *m1,
	                      uint32_t *m2, uint32_t *m3);
	static void Transform2(__m128i *s, uint32_t *m0, uint32_t *m1,
	                       uint32_t *m2, uint32_t *m3);
};

/* ripemd160sse: SSE4.1 implementation processing 2 blocks in parallel */
class ripemd160sse {
public:
	static void Initialize(__m128i *s);
	static void Transform(__m128i *s, uint8_t **data);
};
