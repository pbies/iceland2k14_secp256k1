#pragma once
#include <stdint.h>
#include <string>
#include <vector>

#define BISIZE 256
#define NB64BLOCK (BISIZE/64)
#define NB32BLOCK (BISIZE/32)

class Int {
public:
	Int();
	Int(int64_t i64);
	Int(uint64_t u64);
	Int(Int *a);

	union {
		uint32_t bits[NB32BLOCK + 2];
		uint64_t bits64[NB64BLOCK + 1];
		uint8_t bytes[NB64BLOCK * 8 + 8];
	};

	// Comparison
	bool IsGreater(Int *a);
	bool IsGreaterOrEqual(Int *a);
	bool IsLower(Int *a);
	bool IsLowerOrEqual(Int *a);
	bool IsEqual(Int *a);
	bool IsZero();
	bool IsOne();
	bool IsStrictPositive();
	bool IsPositive();
	bool IsNegative();
	bool IsEven();
	bool IsOdd();
	bool operator==(Int a);

	// Arithmetic
	void Add(Int *a);
	void Add(Int *a, Int *b);
	void Add(uint64_t a);
	void AddOne();
	void AddC(Int *a);
	void AddCh(Int *a, uint64_t carry);
	void AddCh(Int *a, uint64_t carry, Int *b, uint64_t bcarry);
	void AddAndShift(Int *a, Int *b, uint64_t cH);
	void Sub(Int *a);
	void Sub(Int *a, Int *b);
	void Sub(uint64_t a);
	void SubOne();
	void Neg();
	void Abs();
	void Mult(Int *a);
	void Mult(Int *a, Int *b);
	void Mult(uint64_t a);
	void Mult(Int *a, uint64_t b);
	void Mult(Int *a, uint32_t b);
	void IMult(int64_t a);
	void IMult(Int *a, int64_t b);
	void MultModN(Int *a, Int *b, Int *n);
	void Div(Int *a, Int *b = NULL);
	void Mod(Int *a);
	void Rand(int nbit);
	void Rand(Int *n);
	void DivStep62(Int *u, Int *v, int64_t *eta, int *pos, int64_t *f0, int64_t *g0, int64_t *f1, int64_t *g1);
	void GCD(Int *a);
	Int *GetR();
	Int *GetR2();
	Int *GetR3();
	Int *GetR4();
	static Int *GetFieldCharacteristic();
	static void SetupField(Int *n, Int *R = NULL, Int *R2 = NULL, Int *R3 = NULL, Int *R4 = NULL);
	static void InitK1(Int *order);

	// Modular arithmetic
	void ModAdd(Int *a);
	void ModAdd(Int *a, Int *b);
	void ModAdd(uint64_t a);
	void ModSub(Int *a);
	void ModSub(Int *a, Int *b);
	void ModSub(uint64_t a);
	void ModNeg();
	void ModDouble();
	void ModMul(Int *a);
	void ModMul(Int *a, Int *b);
	void ModSquare(Int *a);
	void ModCube(Int *a);
	void ModInv();
	void ModExp(Int *e);
	void ModSqrt();
	bool HasSqrt();
	bool ModPositiveK1();
	void ModMulK1(Int *a);
	void ModMulK1(Int *a, Int *b);
	void ModSquareK1(Int *a);
	void ModAddK1order(Int *a);
	void ModAddK1order(Int *a, Int *b);
	void ModSubK1order(Int *a);
	void ModNegK1order();
	void ModMulK1order(Int *a);
	void MontgomeryMult(Int *a);
	void MontgomeryMult(Int *a, Int *b);

	// Bit operations
	void ShiftL(uint32_t n);
	void ShiftR(uint32_t n);
	void ShiftL32Bit();
	void ShiftR32Bit();
	void ShiftL64Bit();
	void ShiftR64Bit();
	void ShiftL64BitAndSub(Int *a, int n);
	void SwapBit(int i);
	void MaskByte(int n);
	uint32_t GetBit(uint32_t n);
	uint32_t GetLowestBit();
	uint32_t GetSize();
	uint32_t GetSize64();
	uint32_t GetBitLength();

	// Byte/word access
	uint8_t GetByte(int i);
	void SetByte(int i, uint8_t b);
	uint32_t GetInt32();
	void SetInt32(uint32_t v);
	void SetDWord(int i, uint32_t v);
	void SetQWord(int i, uint64_t v);
	void Set(Int *a);
	void Set32Bytes(uint8_t *bytes);
	void Get32Bytes(uint8_t *bytes);
	void Set32InputBytes(uint8_t *bytes);
	void SetBase10(const char *value);
	void SetBase16(const char *value);
	void SetBaseN(int n, const char *charset, const char *value);

	// String conversion
	std::string GetBase10();
	std::string GetBase16();
	std::string GetBase2();
	std::string GetBaseN(int n, char *charset);
	std::string GetBlockStr();
	std::string GetC64Str(int nbDigit);

	// Matrix operations
	void MatrixVecMul(Int *u, Int *v, int64_t _11, int64_t _12, int64_t _21, int64_t _22);
	void MatrixVecMul(Int *u, Int *v, int64_t _11, int64_t _12, int64_t _21, int64_t _22, uint64_t *carry1, uint64_t *carry2);

	// Utilities
	void CLEAR();
	void CLEARFF();
	bool IsProbablePrime();
	double ToDouble();
	bool Check();
	bool CheckInv(Int *a);
};
