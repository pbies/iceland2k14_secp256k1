#pragma once
#include <stdint.h>
#include <string>

#ifdef __cplusplus
extern "C" {
#endif

/* getp2pkh_info: given a coin index (0-based), fills out the P2PKH version byte.
 * coin_idx: integer index into coin table (see library source for table)
 * version:  output P2PKH version byte
 * Returns nothing; sets *version. */
void getp2pkh_info(int coin_idx, int *version);

/* getp2sh_info: given a coin index, fills out the P2SH version byte.
 * coin_idx: integer index into coin table
 * version:  output P2SH version byte */
void getp2sh_info(int coin_idx, int *version);

/* getb32_info: given a coin index, sets *hrp to the bech32 HRP string.
 * coin_idx: integer index into coin table
 * hrp:      output pointer set to static HRP string (e.g. "bc", "ltc") */
void getb32_info(int coin_idx, const char **hrp);

/* CheckAddress: check if address matches a pubkey on secp256k1
 * addr:    address string to check
 * pubhex:  hex-encoded public key (compressed or uncompressed) */
bool CheckAddress(void *secp, std::string addr, std::string pubhex);

/* bech32_encode / bech32_decode wrappers */
bool bech32_encode(char *output, const char *hrp, const uint8_t *data, size_t data_len);
bool bech32_decode(char *hrp, uint8_t *data, size_t *data_len, const char *input);
bool bech32_decode_nocheck(uint8_t *data, size_t *data_len, const char *input);
bool segwit_addr_encode(char *output, const char *hrp, int witver, const uint8_t *prog, size_t prog_len);
bool segwit_addr_decode(int *witver, uint8_t *prog, size_t *prog_len, const char *hrp, const char *addr);
uint32_t bech32_polymod_step(uint32_t pre);

/* Base58 encode/decode */
bool DecodeBase58(const char *str, std::vector<uint8_t> &vch);
bool DecodeBase58(const std::string &str, std::vector<uint8_t> &vch);
std::string EncodeBase58(const uint8_t *pbegin, const uint8_t *pend);
std::string EncodeBase58(const std::vector<uint8_t> &vch);

#ifdef __cplusplus
}
#endif
