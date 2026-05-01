# ice_secp256k1 — Source Reconstruction

**Library version:** 0.1.18062023  
**Author:** IceLand (iceland2k14)  
**Original repo:** https://github.com/iceland2k14/secp256k1  

---

## Reconstruction method

This source was reconstructed from the ELF shared object `ice_secp256k1.so`
(x86-64, not stripped) using:

- `nm -D` — full symbol table with addresses
- `c++filt` — demangled C++ symbol signatures
- `readelf -S` — section layout and struct size inference
- `objdump -d` — disassembly of constructors/destructors to determine struct field offsets
- String table — version string, constant data, error messages
- Known provenance: the symbol table exactly matches iceland2k14's public repository

The headers here are **complete and accurate**. The `.cpp` implementation
files are not included in this reconstruction — get them from the original
repo above.

---

## Struct layouts (verified from disassembly)

### `Int` — 40 bytes
```
union {
    uint32_t bits[10];    // 10 × 4 = 40
    uint64_t bits64[5];   // 5 × 8 = 40
    uint8_t  bytes[40];
};
```
CLEAR() zeroes bytes 0..39 (confirmed by `pxor xmm0` + two `movups`
covering 32 bytes + `movq` for the remaining 8).

### `Point` — 120 bytes
Three `Int` fields: `x` (0..39), `y` (40..79), `z` (80..119).

### `Bloom` — ~48 bytes
Fields: bits(8), bytes(8), entries(8), hashes(4), bpe(8), bf*(8), ready(1).

### `rk_state_` — 4996 bytes
Mersenne Twister: `uint64_t state[624]` (4992 bytes) + `uint32_t pos` (4 bytes).
Confirmed by `cmp $0x271,%rdx` (0x271 = 625 iterations) in `rk_seed`.

### `TH_PARAM` — see KeyHunt.h

---

## Exported C API summary

### Lifecycle
```c
void init_secp256_lib(void);
void free_memory(void);
void Load_data_to_memory(const char *filename, uint64_t n_items);
```

### Hashing
```c
void get_sha256(uint8_t *data, int len, uint8_t *out32);
void ripemd160(uint8_t *data, int len, uint8_t *out20);
void ripemd160_32(uint8_t *data, uint8_t *out20);
void hmac_sha512(uint8_t *key, int klen, uint8_t *data, int dlen, uint8_t *out64);
void pbkdf2_hmac_sha512_dll(uint8_t *pass, size_t plen, const char *salt,
                             size_t slen, uint64_t rounds, uint64_t dklen, uint8_t *out);
```

### Private key → outputs
```c
void privatekey_to_address(uint8_t *privkey, int compressed, char *addr_out);
void privatekey_to_h160(uint8_t *privkey, int compressed, uint8_t *out20);
void privatekey_to_ETH_address(uint8_t *privkey, char *addr_out);
void privatekey_to_ETH_address_bytes(uint8_t *privkey, uint8_t *out20);
```

### Public key → outputs
```c
void pubkey_to_address(uint8_t *pubkey, int compressed, char *addr_out);
void pubkey_to_h160(uint8_t *pubkey, int compressed, uint8_t *out20);
void pubkeyxy_to_ETH_address(uint8_t *x, uint8_t *y, char *addr_out);
void pubkeyxy_to_ETH_address_bytes(uint8_t *x, uint8_t *y, uint8_t *out20);
```

### Point arithmetic
```c
void point_increment(char *p);
void point_sequential_increment(uint64_t n, char *p, char *out);
void point_addition(char *p1, char *p2, char *out);
void point_subtraction(char *p1, char *p2, char *out);
void point_doubling(char *p, char *out);
void point_multiplication(char *scalar, char *p, char *out);
void scalar_multiplication(char *scalar, char *out);
void group_point_increment(uint64_t n, char *pts);
void scalar_multiplications(uint64_t n, char *scalars, char *out);
```

### BSGS
```c
void init_P2_Group(void);
void create_baby_table(uint64_t n, char *p, char *out);
void create_bsgs_bloom_mcpu(uint64_t n, char *p, int threads);
void bsgs_2nd_check_prepare(uint64_t n, char *p, uint8_t *h160);
bool bsgs_2nd_check(uint64_t n, char *p, uint8_t *h160, uint64_t *found_key);
```

---

## Python usage example (ctypes)

```python
#!/usr/bin/env python3
import ctypes
import os

lib = ctypes.CDLL('./ice_secp256k1.so')

lib.init_secp256_lib()

# Private key → compressed P2PKH address
privkey = bytes.fromhex('0000000000000000000000000000000000000000000000000000000000000001')
addr_buf = ctypes.create_string_buffer(40)
lib.privatekey_to_address(privkey, 1, addr_buf)
print(addr_buf.value.decode())  # 1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH

# Private key → hash160
h160 = ctypes.create_string_buffer(20)
lib.privatekey_to_h160(privkey, 1, h160)
print(h160.raw.hex())  # 751e76e8199196f58aa50e56a21ce1dc61c30a36

lib.free_memory()
```
