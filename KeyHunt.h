#pragma once
#include "Secp256K1.h"
#include "Bloom.h"
#include "Int.h"
#include "Point.h"
#include <string>
#include <vector>

/* TH_PARAM: thread parameter block for CPU/GPU search threads */
struct TH_PARAM {
	KeyHunt    *obj;         /* owner object */
	int         threadId;
	bool        isRunning;
	bool        hasStarted;
	bool        isAlive;
	int         gpuId;
	int         gridSize;
	int         blockSize;
};

class KeyHunt {
public:
	/* Constructor:
	 * outputFile:   path to output file for found keys
	 * hashVec:      vector of 20-byte hash160 targets (concatenated)
	 * useGpu:       enable GPU search
	 * gridSize:     CUDA grid size (GPU only)
	 * seed:         random seed string
	 * compressed:   use compressed public keys
	 * targetValue:  bloom filter target count
	 * bloomBits:    bloom filter bit count (log2)
	 * start:        hex string start of search range
	 * end:          hex string end of search range (may be empty)
	 * stop:         reference flag; set to true to stop search
	 */
	KeyHunt(const std::string &outputFile,
	        const std::vector<uint8_t> &hashVec,
	        bool useGpu,
	        bool compressed,
	        const std::string &seed,
	        uint32_t bloomBits,
	        bool gpuMode,
	        const std::string &start,
	        const std::string &end,
	        bool &stop);

	~KeyHunt();

	/* Start CPU+GPU search.
	 * nCpu/nGpu:    number of CPU/GPU threads to use
	 * gpuIds:       list of GPU device IDs
	 * gridSizes:    CUDA grid sizes per GPU
	 * stop:         reference stop flag */
	void Search(int nCpu,
	            std::vector<int> gpuIds,
	            std::vector<int> gridSizes,
	            bool &stop);

	/* Thread entry points */
	void FindKeyCPU(TH_PARAM *p);
	void FindKeyGPU(TH_PARAM *p);

	/* Thread state queries */
	bool isAlive(TH_PARAM *p);
	bool hasStarted(TH_PARAM *p);

	/* CPU/GPU counts */
	int getCPUCount();
	int getGPUCount();

	void SetupRanges(uint32_t nthread);

	void getCPUStartingKey(int threadId, Int &key, Int &count, Point &startPoint);
	void getGPUStartingKeys(int threadId, Int &key, Int &count,
	                        int gridSize, int blockSize,
	                        Int *keys, Point *points);

	bool checkAddresses(bool useSSE, Int privKey, int offset, Point p);
	bool checkAddresses2(bool useSSE, Int privKey, int offset, Point p);
	void checkAddressesSSE(bool useSSE, Int privKey, int offset,
	                       Point p0, Point p1, Point p2, Point p3);
	void checkAddressesSSE2(bool useSSE, Int privKey, int offset,
	                        Point p0, Point p1, Point p2, Point p3);

	bool MatchHash160(uint32_t *h160);
	bool CheckBloomBinary(const uint8_t *h160);

	bool checkPrivKey(std::string addr, Int &key, int keyType, bool isComp, bool isP2SH);

	void output(std::string addr, std::string pKey, std::string pubKey);

	std::string GetHex(std::vector<uint8_t> &buffer);
	std::string formatThousands(uint64_t n);

	void toTimeStr(int sec, char *timeStr);

private:
	std::string   outputFile;
	bool          useGpu;
	bool          compressed;
	bool          gpuMode;
	uint32_t      bloomBits;

	Secp256K1    *secp;
	Bloom        *bloom;

	Int           startKey;
	Int           endKey;
	Int           rangeWidth;
	Int           rangePer;

	/* Per-thread starting keys (allocated in SetupRanges) */
	Int          *threadKeys;

	int           cpuCount;
	int           gpuCount;
	bool         *found;

	/* Output file handle */
	FILE         *outfp;
};
