#pragma once
/*
 * ice_secp256k1 - secp256k1 Bitcoin utility library
 * Version: 0.1.18062023
 * Author: IceLand (iceland2k14)
 *
 * C API for use from Python (ctypes/cffi) and other languages.
 * All functions use C linkage.
 *
 * Point layout in memory (passed as char* to C functions):
 *   bytes [0..31]   = x coordinate (little-endian 256-bit Int)
 *   bytes [32..63]  = y coordinate (little-endian 256-bit Int)
 *   bytes [64..95]  = z coordinate (little-endian 256-bit Int)
 *
 * Int layout: 40 bytes (5 x uint64_t, little-endian).
 * Compressed pubkey: 33 bytes (02/03 prefix + 32-byte X).
 * Uncompressed pubkey: 65 bytes (04 prefix + 32-byte X + 32-byte Y).
 */

#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* =========================================================
 * Library info
 * ========================================================= */

/* Prints version string to stdout */
void version(void);

/* =========================================================
 * Library initialisation (must call before any secp256k1 ops)
 * ========================================================= */

void init_secp256_lib(void);
void free_memory(void);

/* Load BSGS/bloom data into memory.
 * filename: path to .bin target file
 * n_items:  number of hash160 items to allocate for */
void Load_data_to_memory(const char *filename, uint64_t n_items);

/* =========================================================
 * RNG
 * ========================================================= */

typedef struct {
	uint64_t state[625]; /* Mersenne Twister state, 624 uint64 + index */
	uint32_t pos;
} rk_state_;

void  rseed(uint64_t seed);
void  rk_seed(uint64_t seed, rk_state_ *state);
double rnd(void);
long   rndl(void);

/* =========================================================
 * Hash functions
 * ========================================================= */

void get_sha256(uint8_t *data, int len, uint8_t *out32);
void sha256(uint8_t *data, int len, uint8_t *out32);
void sha256_33(uint8_t *data, uint8_t *out32);
void sha256_65(uint8_t *data, uint8_t *out32);
void sha256_checksum(uint8_t *data, int len, uint8_t *out4);
void sha512(uint8_t *data, int len, uint8_t *out64);
void ripemd160(uint8_t *data, int len, uint8_t *out20);
void ripemd160_32(uint8_t *data, uint8_t *out20);

/* SSE4 batched hashing: processes 4 inputs in parallel.
 * Each s_* is a 32-byte hash state array (uint32_t[8]).
 * Each d_* is a pointer to the input data block. */
void sha256sse_1B(uint32_t *s0, uint32_t *s1, uint32_t *s2, uint32_t *s3,
                  uint8_t *d0, uint8_t *d1, uint8_t *d2, uint8_t *d3);
void sha256sse_2B(uint32_t *s0, uint32_t *s1, uint32_t *s2, uint32_t *s3,
                  uint8_t *d0, uint8_t *d1, uint8_t *d2, uint8_t *d3);
void sha256sse_checksum(uint32_t *s0, uint32_t *s1, uint32_t *s2, uint32_t *s3,
                        uint8_t *d0, uint8_t *d1, uint8_t *d2, uint8_t *d3);

void ripemd160sse_32(uint8_t *d0, uint8_t *d1, uint8_t *d2, uint8_t *d3,
                     uint8_t *d4, uint8_t *d5, uint8_t *d6, uint8_t *d7);

/* HMAC-SHA512 */
void hmac_sha512(uint8_t *key, int keylen, uint8_t *data, int datalen, uint8_t *out64);

/* PBKDF2-HMAC-SHA512
 * password/passlen: password bytes
 * salt/saltlen:     salt bytes
 * rounds:           iteration count (e.g. 2048 for BIP39)
 * dklen:            derived key length in bytes (e.g. 64)
 * out:              output buffer of dklen bytes */
void pbkdf2_hmac_sha512_dll(uint8_t *password, size_t passlen,
                             const char *salt, size_t saltlen,
                             uint64_t rounds, uint64_t dklen,
                             uint8_t *out);

/* PBKDF2 on a list of mnemonics.
 * count: number of mnemonic strings
 * mnemonics: array of mnemonic C strings
 * passphrase: BIP39 passphrase (may be "")
 * out: preallocated buffer of count*64 bytes */
void pbkdf2_hmac_sha512_list(int count, const char **mnemonics,
                              const char *passphrase, uint8_t *out);

/* =========================================================
 * Base58 / Bech32
 * ========================================================= */

void b58_encode(const uint8_t *data, size_t len, char *out);
bool b58_decode(const char *str, uint8_t *out, size_t *outlen);
bool bech32_address_decode(const char *addr, uint8_t *progbytes, size_t *proglen);

/* =========================================================
 * Private key → address / hash160
 * ========================================================= */

/* privkey:   32-byte raw private key (big-endian)
 * compressed: 1 = compressed pubkey, 0 = uncompressed
 * addr_out:  output buffer, ≥ 35 bytes for P2PKH address string */
void privatekey_to_address(uint8_t *privkey, int compressed, char *addr_out);

/* cointype: 0=BTC, 2=LTC, 5=DOGE, etc. (BIP44 slip-0044 version byte) */
void privatekey_to_coinaddress(uint8_t *privkey, int compressed,
                                int cointype, char *addr_out);

/* out20: 20-byte hash160 output */
void privatekey_to_h160(uint8_t *privkey, int compressed, uint8_t *out20);

/* ETH: Keccak256 of uncompressed pubkey, last 20 bytes */
void privatekey_to_ETH_address(uint8_t *privkey, char *addr_out);
void privatekey_to_ETH_address_bytes(uint8_t *privkey, uint8_t *out20);

/* =========================================================
 * Public key → address / hash160
 * ========================================================= */

/* pubkey: 33-byte compressed OR 65-byte uncompressed pubkey */
void pubkey_to_address(uint8_t *pubkey, int compressed, char *addr_out);
void pubkey_to_h160(uint8_t *pubkey, int compressed, uint8_t *out20);

/* pubkey_x, pubkey_y: 32-byte X and Y coordinates separately */
void pubkeyxy_to_ETH_address(uint8_t *pubkey_x, uint8_t *pubkey_y, char *addr_out);
void pubkeyxy_to_ETH_address_bytes(uint8_t *pubkey_x, uint8_t *pubkey_y, uint8_t *out20);

/* =========================================================
 * Point operations (raw Int / Point structs)
 * ========================================================= */

/* Returns a 120-byte Point (x=40, y=40, z=40) allocated with malloc.
 * Caller must free_memory() or free() the result.
 * bytes: 33-byte compressed or 65-byte uncompressed pubkey */
char *GetPointfrombytes(char *bytes);

/* Two-pubkey variant: returns two concatenated Points (240 bytes) */
char *GetPointfrombytes(char *bytes1, char *bytes2);

/* bytes: 32-byte raw private key scalar (little-endian Int format) */
char *GetIntfrombytes(char *bytes);

/* Get public key hex from a Point struct */
char *GetPublicKeyHexchar(bool compressed, Point &p);

/* Negate a point (Y = -Y mod P) */
Point Neg_Point(Point p);

/* =========================================================
 * Sequential / batch point operations
 * =========================================================
 *
 * All functions below operate on Point structs in the
 * internal Int layout (x/y/z each 40 bytes).
 *
 * n:     number of steps / points
 * p:     starting Point
 * pts:   output array of Points (caller allocates n * 120 bytes)
 */

/* Increment/decrement a single point by G */
void point_increment(char *point_inout);
void point_sequential_increment(uint64_t n, char *point_inout, char *out);
void point_sequential_decrement(uint64_t n, char *point_inout, char *out);

/* P2 sequential (increments by 2G each step) */
void point_sequential_increment_P2(uint64_t n, char *point_inout, int stride, char *out);

/* Multicore P2 sequential */
void point_sequential_increment_P2_mcpu(uint64_t n, char *point_inout, int stride);

/* Point arithmetic */
void point_addition(char *p1, char *p2, char *out);
void point_subtraction(char *p1, char *p2, char *out);
void point_doubling(char *p, char *out);
void point_negation(char *p, char *out);
void point_multiplication(char *scalar, char *p, char *out);
void scalar_multiplication(char *scalar, char *out);

/* Loop: compute p + i*G for i in [0, n) writing each hash160 to out
 * out: n * 20 byte buffer */
void point_loop_addition(uint64_t n, char *p, char *out);
void point_loop_subtraction(uint64_t n, char *p, char *out);

/* Vector addition: adds G_vector to each point in array */
void point_vector_addition(uint64_t n, char *pts, char *out);

/* group_point_increment: batch increment using IntGroup modular inverse trick
 * n: batch size
 * pts: input/output array of n Points */
void group_point_increment(uint64_t n, char *pts);

/* =========================================================
 * Scalar multiplication batch
 * ========================================================= */

/* n scalars × base point → n public points
 * scalars: n * 40-byte Int array
 * out:     n * 120-byte Point array */
void scalar_multiplications(uint64_t n, char *scalars, char *out);

/* =========================================================
 * Private key loop → hash160 (for scanning)
 *
 * Iterates over n consecutive private keys starting at key,
 * computing hash160 for each, and checking against the
 * bloom filter loaded by Load_data_to_memory.
 * Matches are written to found.txt.
 *
 * key:        40-byte Int (starting private key scalar)
 * compressed: 1=compressed, 0=uncompressed
 * n:          number of keys to check
 * ========================================================= */
void privatekey_loop_h160(char *key, int compressed, uint64_t n);
void privatekey_loop_h160_sse(char *key, int compressed, uint64_t n);

/* =========================================================
 * ETH address sequential from pubkey
 * ========================================================= */

void pubkey_sequential_ETH_address(uint64_t n, char *point_inout, char *out);

/* =========================================================
 * Group/batch ETH address generation
 * ========================================================= */

void privatekey_group_to_ETH_address(uint64_t n, char *keys, char *out);
void privatekey_group_to_ETH_address_bytes(uint64_t n, char *keys, uint8_t *out);

/* =========================================================
 * BSGS (Baby-step Giant-step) support
 * ========================================================= */

void init_P2_Group(void);

/* Create baby-step lookup table
 * n:    number of baby steps
 * p:    starting point
 * out:  n * 20-byte hash160 array */
void create_baby_table(uint64_t n, char *p, char *out);

/* Bloom filter BSGS operations */
void create_bsgs_bloom_mcpu(uint64_t n, char *p, int num_threads);
void bloom_check_add_mcpu(uint64_t n, char *p, int num_threads);

/* Second-pass BSGS check after bloom hit */
void bsgs_2nd_check_prepare(uint64_t n, char *p, uint8_t *hash160);
bool bsgs_2nd_check(uint64_t n, char *p, uint8_t *hash160, uint64_t *found_key);

/* =========================================================
 * Bloom filter helpers
 * ========================================================= */

bool CheckBloomBinary(const uint8_t *h160);
bool check_collision(uint8_t *h160);
bool test_bit_set_bit(uint8_t *bf, uint32_t x, int set_bit);
void bloom_check_add(uint8_t *bf, uint32_t bits, int n_hashes,
                     const uint8_t *key, int keylen, int *found);
void bloom_batch_add(uint64_t n, uint8_t *h160s, uint8_t *bf,
                     uint32_t bits, int n_hashes);

/* =========================================================
 * Address hash utility
 * ========================================================= */

/* hash_to_address: takes 20-byte hash160, returns base58check string */
void hash_to_address(uint8_t *hash160, int version_byte, char *addr_out);

/* =========================================================
 * X-coordinate to Y coordinate
 * ========================================================= */

/* Recover Y from X on secp256k1 curve.
 * x_bytes: 32-byte big-endian X coordinate
 * odd:     1=odd Y, 0=even Y
 * y_out:   32-byte output for Y */
void get_x_to_y(uint8_t *x_bytes, int odd, uint8_t *y_out);

/* Endomorphism shortcuts */
void pub_endo1(char *p, char *out);
void pub_endo2(char *p, char *out);

/* =========================================================
 * Utility
 * ========================================================= */

char *tohex(char *data, int len);
std::string formatThousands(uint64_t n);
std::string GetTimeStr(double seconds);

/* getInts: parse n hex private key strings from args into Int array
 * argc/argv: command-line style
 * out:       n * 40-byte Int array */
void getInts(int n, char **argv, char *out);

#ifdef __cplusplus
}
#endif
