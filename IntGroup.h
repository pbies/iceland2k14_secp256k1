#pragma once
#include "Int.h"

/* IntGroup: batch modular inverse using Montgomery's trick.
 * Reduces cost of n ModInv calls to 3(n-1) multiplications + 1 inverse. */
class IntGroup {
public:
	IntGroup(int size);
	~IntGroup();

	void Set(Int *pts);
	void ModInv();

private:
	Int *ints;   /* pointer to array of Int (not owned) */
	Int *subs;   /* scratch prefix-product array (owned) */
	int  n;
};
