#pragma once
#include "Point.h"
#include "Int.h"
#include <string>
#include <vector>

class Secp256K1 {
public:
	Secp256K1();
	~Secp256K1();

	void Init();
	void Check();

	// Public key operations
	Point ComputePublicKey(Int *privKey);
	Point ComputePublicKey(Int *privKey, bool compress);
	void ComputePublicKeys(std::vector<Int> &privKeys);

	// Address generation
	std::string GetAddress(bool compressed, bool useHash160, Point &pubKey);
	std::string GetAddress(bool compressed, bool useHash160, uint8_t *h160);
	std::string GetAddress(bool compressed, bool useHash160,
		uint8_t *h160a, uint8_t *h160b, uint8_t *h160c, uint8_t *h160d);

	// Hash160 (RIPEMD160(SHA256(pubkey)))
	void GetHash160(bool compressed, bool useHash160, Point &pubKey, uint8_t *h160out);
	void GetHash160(bool compressed, bool useHash160,
		Point &p0, Point &p1, Point &p2, Point &p3,
		uint8_t *h0, uint8_t *h1, uint8_t *h2, uint8_t *h3);

	// Alt addresses
	std::string GetAltAddress(int type, bool compressed, bool useHash160, Point &pubKey);
	std::string GetPrivAddress(bool compressed, Int &key);
	std::string GetPublicKeyHex(bool compressed, Point &pubKey);
	bool CheckPudAddress(std::string addr);

	// Key parsing
	Point DecodePrivateKey(char *str, bool *compressed);
	Point ParsePublicKeyHex(std::string pubHex, bool &compressed);
	Point ParseUpub(std::string upub);
	int GetByte(std::string &str, int pos);
	Point GetY(Int x, bool odd);
	Int X_to_Y(Int x, bool odd);
	bool bech32_coinaddress_decode(int witver, char *hrp, uint8_t *scriptpubkey);

	// EC arithmetic
	Point Add(Point &p1, Point &p2);
	Point Add2(Point &p1, Point &p2);
	Point Double(Point &p);
	Point DoubleDirect(Point &p);
	Point NextKey(Point &p);
	void ScalarMultiplication(Point &p, Int k);
	void AddDirect(Point &p1, Point &p2);
	void AddDirectWithZero(Point &p1, Point &p2);
	void ECE(Point &p);
	void AddDirect(std::vector<Point> &pts, std::vector<Point> &src);
	void GetEndomorphism1(Point &p);
	void GetEndomorphism2(Point &p);

	// Precomputed tables (5 * 256 entries)
	Point GTable[5 * 256];

	// Curve params (public for C API access)
	Int order;
	Int Gx;
	Int Gy;
	Int P;
	Int beta;
	Int lambda;
	Int beta2;
	Int lambda2;
};
