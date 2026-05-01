#pragma once
#include "Int.h"
#include <string>

class Point {
public:
	Point();
	Point(const Point &p);
	Point(Int *x, Int *y, Int *z);
	Point(Int *x, Int *y);
	~Point();

	Int x;
	Int y;
	Int z;

	bool isZero();
	bool equals(Point &p);
	void Set(Point &p);
	void Set(Int *x, Int *y, Int *z);
	void Clear();
	void Reduce();
	void Neg();

	void Add(Point &p);
	void Double();
	void Sub(Point &p);
	void Mul(Int &k);

	std::string toString();
	std::string toPubKey();
};
